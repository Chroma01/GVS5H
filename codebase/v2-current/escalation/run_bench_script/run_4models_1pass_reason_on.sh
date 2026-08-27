#!/usr/bin/env bash
# 4 models x {single, manager}, LCB-100 (pinned ids), 1 pass, reasoning ON.
# FIRST-PARTY PROVIDERS ONLY -- no OpenRouter. OpenRouter's routing was the main source of
# run-to-run noise (silent provider swaps, clamped output caps, stalls), so each arm here
# talks to exactly one backend and a run is reproducible against it.
#
#   q36l   groq:qwen3.6-27b-vllm     local vLLM :8215 via litellm :8216   (no key cost)
#   luna   openai:gpt-5.6-luna       OpenAI            OPENAI_API_KEY
#   q38    dashscope:qwen3.8         Alibaba Model Studio  DASHSCOPE_API_KEY
#   opus5  anthropic:claude-opus-5   Anthropic         ANTHROPIC_API_KEY
#
# THE ARMS ARE NOT SYMMETRIC. Two differences are imposed by the providers, not chosen:
#
#  1. OUTPUT CAP. Opus 5 hard-caps output at 128K; anthropic_chat clamps a larger request
#     and records `cap_clamped_to`. So 200k is unreachable on that arm and a common 128k
#     cap is the only like-for-like setting across all four. Run CAP=200000 if you would
#     rather let the two Qwen arms stretch and accept that opus5 is capped lower.
#
#  2. THINKING TEXT. Only the two Qwen arms return the real chain of thought (vLLM's
#     --reasoning-parser splits it into reasoning_content, and DashScope returns the same
#     field). OpenAI and Anthropic never return raw reasoning tokens -- the opus5 arm
#     records Anthropic's SUMMARY (meta.reasoning_is_summary=1) and the luna arm records
#     nothing but a reasoning-token COUNT. Any analysis of thinking length/content holds
#     for q36l and q38 only.
#
# Problem set is PINNED to the same 100 the plotted runs used (escalation/lcb100_hardest_v6.json)
# and the post-run check fails loudly on any drift, so a 4-way plot compares like with like.
set -u
cd /home/persis/model-test

export LCB_RELEASE=release_v6
export HF_HOME=/storage/persis/hf_cache
export MULTIAGENT_MAX_ITERS=10
export MULTIAGENT_MAX_TASKS=12

CAP=${CAP:-128000}                # common output cap; see note 1 above
IDS=escalation/lcb100_hardest_v6.json
OUT=escalation/runs/4models-1pass-reason-on/results
WS=/home/persis/model-test/escalation/runs/4models-1pass-reason-on/ws
mkdir -p "$OUT" "$WS"

set -a; [ -f escalation/.env ] && . escalation/.env; set +a
# .env uses a lowercase name; the SDKs and orchestrator both want the canonical one.
export OPENAI_API_KEY="${OPENAI_API_KEY:-${openai_api_key:-}}"

{ echo "sha=$(git rev-parse HEAD)"
  git status --porcelain -- escalation/ | sed 's/^/dirty: /'
  echo "cap=$CAP max_iters=$MULTIAGENT_MAX_ITERS release=$LCB_RELEASE ids=$IDS reasoning=on"
} > "$OUT/run_config.txt"

check() {  # out_json -- ids must match the pinned 100, order included
  IDS="$IDS" python3 -c '
import json, os, sys
want = json.load(open(os.environ["IDS"]))
got = [r["question_id"] for r in json.load(open(sys.argv[1]))["lcb"]["records"]]
if got != want:
    print(f"  !! MISMATCH in {sys.argv[1]}: {len(got)}/{len(want)} ids, "
          f"missing={sorted(set(want)-set(got))[:5]}", file=sys.stderr)
    sys.exit(1)
print(f"  ids OK ({len(got)}/100, order matches)")' "$1"
}

run() {  # tag  engine  parallel  <env assignments...>
  local tag=$1 eng=$2 par=$3; shift 3
  local out="$OUT/${tag}_${eng}.json"
  [ -f "$out" ] && { echo "[skip done] ${tag}_${eng}"; return; }
  echo "[$(date +%H:%M:%S)] start ${tag}_${eng}"
  env "$@" MULTIAGENT_WS="$WS/${tag}_${eng}" \
    uv run --project /home/persis/model-test python escalation/run_bench.py \
    --engine "$eng" --only lcb --lcb 100 --ids-file "$IDS" --parallel "$par" --out "$out" \
    > "/tmp/4m_${tag}_${eng}.log" 2>&1
  echo "[$(date +%H:%M:%S)] done  ${tag}_${eng}"
  check "$out" || echo "  (see /tmp/4m_${tag}_${eng}.log)"
}

# Preflight per arm. A missing key SKIPS that arm loudly rather than letting run_bench.py
# die 100 times; a bad key now surfaces as a hard abort instead of a silent cap reduction
# (openai_chat only shrinks max_tokens on a 400 whose body actually mentions the context).
have() {  # var_name  human_name
  [ -n "${!1:-}" ] && return 0
  echo "[skip] $2: \$$1 is not set"; return 1
}

# --- arm 1: qwen3.6-27b, local vLLM -------------------------------------------------------
# Reasoning is on by default (Qwen3.6 chat template + --reasoning-parser qwen3), so send no
# reasoning field: vLLM rejects reasoning_effort. Key comes from litellm's own config --
# run_lcb.sh's copy has drifted and now fails auth.
LITELLM_KEY="${LITELLM_KEY:-$(grep -m1 'master_key:' /home/persis/litellm/config.yaml | awk '{print $2}')}"
if curl -sf -m 20 http://localhost:8216/v1/chat/completions \
     -H "Authorization: Bearer $LITELLM_KEY" -H 'Content-Type: application/json' \
     -d '{"model":"qwen3.6-27b-vllm","messages":[{"role":"user","content":"ok"}],"max_tokens":4}' \
     > /dev/null; then
  # --parallel 48, sized by KV rather than by the throughput curve. benchmark_results.md
  # measures 772,065 KV tokens per replica across 3 replicas; muse's calls peak near 40k
  # tokens (prompt + output), so ~19 sequences fit per replica = ~57 concurrent before
  # sequences start being preempted and recomputed. 48 stays inside that even if every
  # sequence hits the largest size observed.
  # The box's 16.3k tok/s headline is NOT reachable here: it saturates at ~768 concurrent
  # streams, and --parallel counts problems in flight (one request each), so 100 problems
  # cap concurrency at 100. At 48 the measured aggregate is ~3,065 tok/s.
  # MULTIAGENT_STRICT_FORMAT=1 is REQUIRED here, not optional. Muse-Glimmer answers the
  # problem instead of filling in the manager's response format and emits no "### " headers,
  # so plan and ideation both parse to ZERO items and the manager silently degrades to a
  # single worker round -- no error, just a wrong experiment. Measured on arc196_b: 0 tasks
  # / 0 approaches without it, 4 tasks / 3 approaches and a PASS with it. It cannot be
  # auto-detected because litellm's route name says nothing about the weights behind it.
  for eng in single multiagent; do
    run muse $eng 48 \
      ESCALATION_OPENAI_BASE="http://localhost:8216/v1/chat/completions" \
      GROQ_API_KEY="$LITELLM_KEY" \
      ESCALATION_GROQ_REASONING="" \
      ESCALATION_CLOUD_MAX_TOKENS="$CAP" \
      ESCALATION_CLOUD_TIMEOUT=7200 \
      MULTIAGENT_STRICT_FORMAT=1 \
      MULTIAGENT_MODEL="groq:small-model"
  done
else
  echo "[skip] q36l: litellm probe failed on :8216"
fi

# --- arm 2: GPT-5.6 Luna, OpenAI ----------------------------------------------------------
# GPT-5 series renames max_tokens -> max_completion_tokens and rejects a non-default
# temperature; the openai: branch handles both. Reasoning effort is left at the model
# default (set ESCALATION_OPENAI_REASONING=low|medium|high to pin it).
if have OPENAI_API_KEY "luna (gpt-5.6-luna)"; then
  for eng in single multiagent; do
    run luna $eng 32 \
      OPENAI_API_KEY="$OPENAI_API_KEY" \
      ESCALATION_CLOUD_MAX_TOKENS="$CAP" \
      ESCALATION_CLOUD_TIMEOUT=7200 \
      MULTIAGENT_MODEL="openai:gpt-5.6-luna"
  done
fi

# --- arm 3: Qwen3.8-Max, Alibaba Cloud Model Studio (first-party) --------------------------
# Released 2026-08-03: 2.4T-param MoE, ~95B active, 1M context, $2/$6 per MTok. NOTE this is
# a frontier-scale model, NOT a size-peer of the local 30B -- it belongs beside opus5 on the
# plot. The open-weights Qwen3.8-27B checkpoint had not shipped as of 2026-08-12.
#
# UNVERIFIED without a key: `qwen3.8-max` is the expected id but Alibaba also ships -plus and
# -preview variants; confirm against GET $ESCALATION_DASHSCOPE_BASE/../models first.
#
# BASE URL IS REGION-SCOPED. The default below is the legacy international host. Singapore,
# Tokyo, Frankfurt, Hong Kong and Beijing all require YOUR WORKSPACE ID in the hostname, e.g.
#   ESCALATION_DASHSCOPE_BASE=https://<WorkspaceId>.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions
# US (Virginia) is workspace-free: https://dashscope-us.aliyuncs.com/compatible-mode/v1/...
if have DASHSCOPE_API_KEY "q38 (qwen3.8-max)"; then
  for eng in single multiagent; do
    # THINKING_BUDGET IS MANDATORY. max_tokens does not bound thinking on DashScope --
    # measured: max_tokens=100 generated for 5 minutes and never returned; a real prompt ran
    # past 72 min. thinking_budget does bound it exactly (256 -> reasoning_tokens 256).
    # Without it this arm has no cap at all and bills for unbounded reasoning.
    run q38 $eng 4 \
      DASHSCOPE_API_KEY="$DASHSCOPE_API_KEY" \
      ESCALATION_CLOUD_MAX_TOKENS="$CAP" \
      ESCALATION_DASHSCOPE_THINKING_BUDGET="${THINK_BUDGET:-100000}" \
      ESCALATION_CLOUD_TIMEOUT=7200 \
      MULTIAGENT_MODEL="dashscope:qwen3.8-max"
  done
fi

# --- arm 4: Opus 5, Anthropic -------------------------------------------------------------
# Thinking is adaptive and on by default. Output clamps to 128K (see note 1). This is the
# most expensive arm by far: ~2400 calls across both engines at $5/$25 per MTok.
if have ANTHROPIC_API_KEY "opus5 (claude-opus-5)"; then
  for eng in single multiagent; do
    run opus5 $eng 4 \
      ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
      ESCALATION_CLOUD_MAX_TOKENS="$CAP" \
      ESCALATION_CLOUD_TIMEOUT=7200 \
      MULTIAGENT_MODEL="anthropic:claude-opus-5"
  done
fi

echo "[$(date +%H:%M:%S)] ALL 4-MODEL RUNS DONE (skipped arms listed above)"
