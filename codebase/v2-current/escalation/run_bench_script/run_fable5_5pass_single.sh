#!/usr/bin/env bash
# Claude Fable 5, SINGLE-CALL arm only, LCB-100 (pinned ids), 5 independent passes.
# First-party Anthropic Messages API -- no OpenRouter. The paper's Opus-5 rows were served
# through OpenRouter (runs/results_think_high/opus_single.json records
# `openrouter:anthropic/claude-opus-5`), which is the gateway blamed for the run-to-run noise
# in S2.4; this arm talks to Anthropic directly so a pass is reproducible against one backend.
#
# WHY SINGLE-ONLY. No manager arm here, so this run measures the model, not the scaffold. It
# is comparable to the `Single` column of the other 128k/reasoning-on rows -- NOT to their
# deltas, which need both arms.
#
# THREE THINGS ABOUT FABLE 5 THAT ARE NOT LIKE THE OTHER ARMS:
#
#  1. THINKING CANNOT BE TURNED OFF, AND HAS NO BUDGET. `thinking:{type:disabled}` and
#     `{type:enabled,budget_tokens:N}` both return 400. anthropic_chat() already sends
#     `{type:adaptive, display:summarized}`, which is the accepted form -- so this arm is
#     unavoidably reasoning-ON and its `meta["reasoning"]` is Anthropic's SUMMARY, never the
#     raw chain of thought (same caveat as the opus5 arm; cf. the two Qwen arms, which return
#     the real thing) -- transcripts carry `reasoning_is_summary` so the two cannot later be
#     read as the same kind of evidence. Depth is `output_config.effort`, pinned to `high` in
#     orchestrator.py (ANTHROPIC_EFFORT); `high` is also the API default.
#
#  2. 128k IS THE MODEL'S CEILING, not a choice. Fable 5 caps output at 128K, so the cap below
#     is exactly the ceiling and matches the other 128k arms with nothing clamped. Note the cap
#     bounds thinking + answer TOGETHER: a problem that thinks for 128k tokens returns no code
#     and is scored `truncated`, which is the honest outcome and must not be "fixed" by raising
#     the cap -- it cannot go higher.
#
#  3. REFUSALS ARE SCORED, NOT RETRIED, AND NOT FALLEN BACK. Fable 5's classifiers can decline
#     a request (HTTP 200, stop_reason=refusal). Anthropic's own guidance is to pass a
#     `fallbacks` parameter so another model answers instead -- DELIBERATELY NOT DONE HERE: a
#     benchmark cell labelled Fable 5 must contain Fable 5's outcome, and a silent rescue by
#     Opus 4.8 would contaminate the measurement. anthropic_chat() returns the refusal's (empty)
#     text, so it lands as `empty_stop` with `finish_reason=refusal` on the record -- count
#     those before reading the pass@1:
#       jq '[.lcb.records[]|select(.finish_reason=="refusal")]|length' <results>.json
set -u
cd /home/persis/model-test

export LCB_RELEASE=release_v6
export HF_HOME=/storage/persis/hf_cache

CAP=${CAP:-128000}                # == Fable 5's hard output ceiling; see note 2
# PAR is sized by the OUTPUT-token limit, not by requests. Measured on this org: 2000 req/min
# but only 300k output tokens/min, and a problem generates ~16.5k output tokens over ~3.5 min
# (~4.7k tok/min per stream), so ~64 streams already saturate OTPM. Past that the API just
# returns 429s and the SDK backs off -- more concurrency buys no wall clock, only retries.
PAR=${PAR:-50}
REMAIN=${REMAIN:-8}               # release the next pass when this many problems are left
# Retries must outlast a 429 storm. An exhausted call becomes an `infra` record, and those are
# EXCLUDED from grading (run_bench.py), so a rate-limited pass would report pass@1 over fewer
# than 100 problems while the id check still passes -- a silently wrong denominator.
export ESCALATION_CLAUDE_ATTEMPTS=${ESCALATION_CLAUDE_ATTEMPTS:-10}
IDS=escalation/lcb100_hardest_v6.json
OUT=escalation/runs/fable5-5pass-single/results
WS=/home/persis/model-test/escalation/runs/fable5-5pass-single/ws
mkdir -p "$OUT" "$WS"

set -a; [ -f escalation/.env ] && . escalation/.env; set +a

# Preflight. A missing key must abort HERE, not 500 times: anthropic_chat() raises per call,
# so an unset key would burn the whole pass on identical RuntimeErrors.
if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo "FATAL: ANTHROPIC_API_KEY is not set (not in the environment, not in escalation/.env)."
  echo "       This arm is first-party Anthropic; there is no other credential path."
  exit 1
fi

# Confirm the id resolves and the org can call it BEFORE spending a pass. Fable 5 requires
# 30-day data retention -- an org configured below that gets 400 on every request with a
# perfectly valid body, and this probe is where that surfaces.
uv run --project /home/persis/model-test python - <<'PY' || exit 1
import os, sys, anthropic
c = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"], timeout=300)
try:
    with c.messages.stream(model="claude-fable-5", max_tokens=1024,
                           messages=[{"role": "user", "content": "Reply with just: ok"}]) as s:
        m = s.get_final_message()
except Exception as e:
    print(f"FATAL: probe failed: {type(e).__name__}: {str(e)[:300]}", file=sys.stderr)
    sys.exit(1)
print(f"  probe OK: model={m.model} stop={m.stop_reason} out_tokens={m.usage.output_tokens}")
PY

{ echo "sha=$(git rev-parse HEAD)"
  git status --porcelain -- escalation/ | sed 's/^/dirty: /'
  echo "model=anthropic:claude-fable-5 cap=$CAP parallel=$PAR release=$LCB_RELEASE ids=$IDS"
  echo "engine=single passes=5 thinking=adaptive(always on) effort=high(pinned) fallbacks=none"
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

# PIPELINED, not sequential: the next pass is released once the current one has only REMAIN
# problems left, rather than waiting for its tail. The last few problems of a pass run nearly
# alone -- concurrency collapses to single digits while a couple of hard problems think their
# way to the cap -- which would otherwise leave the OTPM budget idle for the length of the
# slowest problem, five times over.
launch() {  # pass -> 0 if started, 1 if skipped
  local p=$1 out="$OUT/fable5_single_p${p}.json"
  [ -f "$out" ] && { echo "[skip done] fable5_single_p${p}"; return 1; }
  echo "[$(date +%H:%M:%S)] start fable5_single_p${p}"
  env ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
      ESCALATION_CLOUD_MAX_TOKENS="$CAP" \
      ESCALATION_CLOUD_TIMEOUT=7200 \
      MULTIAGENT_MODEL="anthropic:claude-fable-5" \
      MULTIAGENT_WS="$WS/fable5_single_p${p}" \
    uv run --project /home/persis/model-test python escalation/run_bench.py \
      --engine single --only lcb --lcb 100 --ids-file "$IDS" --parallel "$PAR" --out "$out" \
      > "/tmp/fable5_single_p${p}.log" 2>&1 &
  return 0
}

wait_almost() {  # pass -- return at <=REMAIN left, or when the pass has finished
  local p=$1 out="$OUT/fable5_single_p${p}.json" log="/tmp/fable5_single_p${p}.log" d
  while true; do
    [ -f "$out" ] && { echo "[$(date +%H:%M:%S)] fable5_single_p${p} finished"; return; }
    # grep -c prints 0 AND exits 1 on no match, so `|| echo 0` would append a second 0 and
    # make the comparison a syntax error -- which fails closed and stalls the pipeline.
    d=0
    if [ -f "$log" ]; then d=$(grep -c 'done (' "$log" 2>/dev/null) || d=0; fi
    if [ "$d" -ge $((100 - REMAIN)) ]; then
      echo "[$(date +%H:%M:%S)] fable5_single_p${p} at ${d}/100 -- releasing next"
      return
    fi
    sleep 30
  done
}

for p in 1 2 3 4 5; do
  launch "$p" && wait_almost "$p"
done
wait

for p in 1 2 3 4 5; do
  out="$OUT/fable5_single_p${p}.json"
  [ -f "$out" ] && { printf 'p%s: ' "$p"; check "$out" || echo "  (see /tmp/fable5_single_p${p}.log)"; }
done

echo "[$(date +%H:%M:%S)] FABLE5 5 SINGLE PASSES DONE"
