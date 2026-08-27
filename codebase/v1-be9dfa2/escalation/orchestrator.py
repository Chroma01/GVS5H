"""Hierarchical multi-model escalation over local ollama.

Configuration (as requested):
  - A ladder of qwen3.5 models ordered by size/capability.
  - For each problem: the SMALLEST model solves, then a second instance of the
    same model critiques. Solver and critic pass the answer back and forth until
    the critic is satisfied (APPROVED) or a per-layer round cap is hit.
  - The satisfied answer is then handed UP to the next (larger) layer as a
    reference candidate, which runs the same solve<->critique loop to improve it.
  - The top layer's approved answer is the final output.

Talks to ollama's /api/chat directly (no extra deps; stdlib urllib only).
"""

import os
import sys
import json
import time
import threading
import urllib.request
import urllib.error

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

# Cloud passthrough: a ladder entry like "groq:openai/gpt-oss-120b" routes to
# Groq's OpenAI-compatible endpoint instead of local ollama. Any provider with
# an OpenAI-compatible /v1/chat/completions works via ESCALATION_OPENAI_BASE.
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
# Disable hidden reasoning by default: the free-tier token/min limit is tiny and
# qwen3.6's <think> blocks burn ~10x the tokens. "none" or "default".
GROQ_REASONING = os.environ.get("ESCALATION_GROQ_REASONING", "none")

# OpenRouter: a ladder/model entry like "openrouter:qwen/qwen3-30b-a3b" routes here.
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
# "none" -> ask OpenRouter to disable reasoning; "" -> leave to model default.
OPENROUTER_REASONING = os.environ.get("ESCALATION_OR_REASONING", "none")

# Size-ordered ladder (small -> large). Names resolved against `ollama list`.
LADDER = os.environ.get(
    "ESCALATION_LADDER",
    "qwen3.5:2b,qwen3.5:9b,qwen3.5:35b,qwen3.5:122b",
).split(",")

MAX_ROUNDS = int(os.environ.get("ESCALATION_MAX_ROUNDS", "2"))  # solver<->critic rounds per layer
THINK = os.environ.get("ESCALATION_THINK", "0") == "1"          # enable model "thinking" (slower)
REQUEST_TIMEOUT = int(os.environ.get("ESCALATION_TIMEOUT", "1200"))
# Cloud calls should be fast; a hung provider must abort quickly and let retry
# re-route to a different provider rather than blocking on the 20-min local cap.
# This is a HARD wall-clock cap (a socket timeout alone doesn't bound total time:
# some providers trickle bytes slowly, keeping the read alive for minutes).
CLOUD_TIMEOUT = int(os.environ.get("ESCALATION_CLOUD_TIMEOUT", "120"))
# Cap generation length so no single call can run away (0 = unset).
CLOUD_MAX_TOKENS = int(os.environ.get("ESCALATION_CLOUD_MAX_TOKENS", "8000"))


def ollama_chat(model, messages, temperature=0.2, num_ctx=16384, meta=None):
    body = {
        "model": model,
        "messages": messages,
        "stream": False,
        "think": THINK,
        "options": {"temperature": temperature, "num_ctx": num_ctx},
    }
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/chat", data=data, headers={"Content-Type": "application/json"}
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as r:
                out = json.loads(r.read())
            if meta is not None:
                meta["finish_reason"] = out.get("done_reason")
                meta["completion_tokens"] = out.get("eval_count")
            return out["message"]["content"]
        except Exception as e:  # noqa: BLE001 - ollama can drop/reload; retry
            if attempt == 2:
                raise
            time.sleep(3 * (attempt + 1))
    return ""


def openai_chat(url, api_key, model, messages, temperature=0.2, extra=None, meta=None):
    """Call an OpenAI-compatible /v1/chat/completions endpoint (e.g. Groq, OpenRouter).

    Each attempt has a HARD wall-clock cap: a watchdog abandons a provider that
    stalls (some trickle bytes slowly and evade the socket timeout) so the retry
    re-routes to a different, faster provider.
    """
    body = {"model": model, "messages": messages, "stream": False, "temperature": temperature}
    if CLOUD_MAX_TOKENS > 0:
        body["max_tokens"] = CLOUD_MAX_TOKENS
    if extra:
        body.update(extra)
    data = json.dumps(body).encode()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        # Groq/Cloudflare returns 403 for urllib's default UA; set an explicit one.
        "User-Agent": "model-test/1.0",
    }

    def _do(box):
        try:
            req = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=CLOUD_TIMEOUT) as r:
                box["out"] = json.loads(r.read())
        except Exception as e:  # noqa: BLE001 - captured for the caller to classify
            box["err"] = e

    for attempt in range(6):
        box = {}
        th = threading.Thread(target=_do, args=(box,), daemon=True)
        th.start()
        th.join(CLOUD_TIMEOUT + 5)
        if th.is_alive():  # hard cap: abandon the stalled provider (daemon thread leaks, dies later)
            if attempt == 5:
                raise TimeoutError(f"cloud call exceeded {CLOUD_TIMEOUT}s on every attempt")
            print(f"    [cloud] hard timeout >{CLOUD_TIMEOUT}s, abandoning provider (attempt {attempt + 1})", file=sys.stderr, flush=True)
            continue
        if "out" in box:
            choice = box["out"]["choices"][0]
            msg = choice["message"]
            finish = choice.get("finish_reason")
            content = msg.get("content") or ""
            # Some hybrid-reasoning models return content=null with text under "reasoning".
            # Trust that fallback ONLY on a clean stop: a call truncated mid-thought
            # (finish_reason=length) has produced no answer, and handing its raw reasoning
            # back as the reply poisons the multi-agent workspace -- the manager then reads
            # 100k chars of stream-of-consciousness as the "current answer" and reissues the
            # same task until MAX_ITERS runs out.
            if not content and finish == "stop":
                content = msg.get("reasoning") or ""
            if finish and finish != "stop":
                # Diagnostic. An abnormal stop -- usually 'length', i.e. hit
                # CLOUD_MAX_TOKENS mid-generation -- leaves an unclosed ```python fence,
                # and extract_code then reads the whole attempt as empty. Log it so a
                # run's empty-code rate is attributable instead of silent.
                ntok = (box["out"].get("usage") or {}).get("completion_tokens")
                print(f"    [cloud] finish_reason={finish} ({len(content)} chars, "
                      f"{ntok} completion tokens)", file=sys.stderr, flush=True)
                if not content:
                    # Deliberately NOT retried: the cause is the token budget, not a
                    # transient fault, so an identical retry just burns the cap again.
                    print("    [cloud] truncated before any content; discarding reasoning-only reply",
                          file=sys.stderr, flush=True)
            if meta is not None:
                meta["finish_reason"] = finish
                meta["completion_tokens"] = (box["out"].get("usage") or {}).get("completion_tokens")
            return content
        e = box.get("err")
        if isinstance(e, urllib.error.HTTPError) and e.code == 429 and attempt < 5:
            ra = e.headers.get("retry-after")
            try:
                wait = float(ra) if ra else min(30.0, 5.0 * (attempt + 1))
            except ValueError:
                wait = min(30.0, 5.0 * (attempt + 1))
            print(f"    [cloud] 429 rate-limited, sleep {wait:.0f}s (attempt {attempt + 1})", file=sys.stderr, flush=True)
            time.sleep(wait + 1)
            continue
        if attempt == 5:
            raise e
        print(f"    [cloud] {type(e).__name__} on attempt {attempt + 1}, retrying", file=sys.stderr, flush=True)
        time.sleep(3 * (attempt + 1))
    return ""


def chat(model, messages, temperature=0.2, num_ctx=16384, meta=None):
    """Dispatch to a cloud provider for prefixed models, else local ollama.

    If `meta` (a dict) is passed, it is populated with {finish_reason, completion_tokens}
    from the underlying call, so callers can classify truncated/empty_stop outcomes.
    """
    if model.startswith("groq:"):
        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY not set but ladder uses a groq: model")
        extra = {"reasoning_effort": GROQ_REASONING} if GROQ_REASONING else None
        return openai_chat(GROQ_URL, GROQ_API_KEY, model[len("groq:"):], messages, temperature, extra, meta)
    if model.startswith("openrouter:"):
        if not OPENROUTER_API_KEY:
            raise RuntimeError("OPENROUTER_API_KEY not set but model uses an openrouter: prefix")
        extra = {"provider": {"sort": "throughput"}}  # prefer fast providers, avoid stalls
        if OPENROUTER_REASONING == "none":
            extra["reasoning"] = {"enabled": False}
        elif OPENROUTER_REASONING in ("low", "medium", "high"):
            extra["reasoning"] = {"effort": OPENROUTER_REASONING}
        # any other value (e.g. "default") -> send nothing; model reasons at its default
        return openai_chat(OPENROUTER_URL, OPENROUTER_API_KEY, model[len("openrouter:"):], messages, temperature, extra, meta)
    return ollama_chat(model, messages, temperature=temperature, num_ctx=num_ctx, meta=meta)


# --- Task specifications ---------------------------------------------------
# A task spec adapts the loop to a domain (code vs math) via prompt fragments.

CODE_SPEC = {
    "kind": "code",
    "solver_system": (
        "You are an elite competitive programmer. Solve the given problem in Python. "
        "Think carefully about algorithmic complexity and edge cases. "
        "Output EXACTLY ONE complete, self-contained Python program inside a single "
        "```python ...``` fenced block, and nothing else after it."
    ),
    "critic_system": (
        "You are a ruthless code reviewer for competitive programming. You are given a "
        "problem statement and a candidate Python solution. Check for: wrong algorithm, "
        "incorrect edge cases, off-by-one errors, wrong time/space complexity for the "
        "constraints, and INPUT/OUTPUT FORMAT mismatches (stdin/stdout vs function). "
        "If and only if the solution is fully correct and complete, reply with exactly "
        "'APPROVED' on the first line. Otherwise reply 'REJECTED' on the first line "
        "followed by a numbered list of concrete, fixable problems."
    ),
}

MATH_SPEC = {
    "kind": "math",
    "solver_system": (
        "You are an elite mathematician solving an AIME problem. The answer is an integer "
        "from 0 to 999. Reason step by step, then on the FINAL line output exactly "
        "'ANSWER: <integer>'."
    ),
    "critic_system": (
        "You are a meticulous math grader. You are given an AIME problem and a candidate "
        "solution. Check the reasoning and the final integer answer for errors. If the "
        "solution is fully correct, reply with exactly 'APPROVED' on the first line. "
        "Otherwise reply 'REJECTED' on the first line followed by the specific errors."
    ),
}


MATH500_SPEC = {
    "kind": "math",
    "solver_system": (
        "You are an elite mathematician. Solve the problem. Reason step by step, then on the FINAL "
        "line output exactly 'ANSWER: <final answer>' with the answer in simplest form (a number or "
        "simplified expression, written as it would appear in a textbook)."
    ),
    "critic_system": (
        "You are a meticulous math grader. Given a problem and a candidate solution, check the "
        "reasoning and final answer. If fully correct, reply exactly 'APPROVED' on the first line; "
        "otherwise reply 'REJECTED' then the specific errors."
    ),
}

GPQA_SPEC = {
    "kind": "math",
    "solver_system": (
        "You are a PhD-level expert in physics, chemistry, and biology answering a multiple-choice "
        "question with options A, B, C, D. Reason carefully, then on the FINAL line output exactly "
        "'ANSWER: <letter>' where <letter> is the single correct option (A, B, C, or D)."
    ),
    "critic_system": (
        "You are a rigorous science reviewer. Given a multiple-choice question and a candidate "
        "answer, verify the reasoning and the chosen letter. If fully correct reply 'APPROVED' on "
        "the first line; otherwise reply 'REJECTED' then the errors."
    ),
}

HLE_SPEC = {
    "kind": "math",
    # 'ANSWER:' rather than upstream HLE's 'Exact Answer:' -- multiagent.py's ANS_RE gates
    # whether a worker may overwrite answer.md, so keep this repo's existing convention.
    "solver_system": (
        "You are answering a question from Humanity's Last Exam: an extremely difficult, "
        "expert-level question that may come from any academic discipline. It may be "
        "multiple-choice or require an exact free-form answer (a number, expression, name, or "
        "short phrase). If it is multiple-choice, answer with the option LETTER only -- note "
        "there may be more than four options. Reason carefully, then finish with exactly "
        "these two lines:\n"
        "ANSWER: <your succinct, exact final answer -- no explanation, no units unless asked>\n"
        "CONFIDENCE: <integer 0-100>"
    ),
    "critic_system": (
        "You are a rigorous expert reviewer across all academic fields. Given a question and a "
        "candidate answer, check the reasoning and the exact final answer for errors. If fully "
        "correct reply 'APPROVED' on the first line; otherwise reply 'REJECTED' then the errors."
    ),
}


def _is_approved(critique):
    return critique.strip().upper().startswith("APPROVED")


def solve_layer(model, problem_text, spec, prior_answer=None, temperature=0.2, log=None):
    """Run the solver<->critic loop for one model layer. Returns final answer text."""
    log = log or (lambda *a, **k: None)

    solver_msgs = [{"role": "system", "content": spec["solver_system"]}]
    if prior_answer:
        user = (
            f"{problem_text}\n\n"
            "A smaller model produced the following candidate solution. Treat it as a "
            "hint only: verify it, fix any mistakes, and produce YOUR OWN best solution.\n\n"
            f"--- candidate ---\n{prior_answer}\n--- end candidate ---"
        )
    else:
        user = problem_text
    solver_msgs.append({"role": "user", "content": user})

    answer = chat(model, solver_msgs, temperature=temperature)
    solver_msgs.append({"role": "assistant", "content": answer})

    for rnd in range(MAX_ROUNDS):
        critique = chat(
            model,
            [
                {"role": "system", "content": spec["critic_system"]},
                {
                    "role": "user",
                    "content": f"PROBLEM:\n{problem_text}\n\nCANDIDATE SOLUTION:\n{answer}",
                },
            ],
            temperature=0.1,
        )
        log(f"    [{model}] round {rnd + 1} critic: {'APPROVED' if _is_approved(critique) else 'rejected'}")
        if _is_approved(critique):
            break
        # solver revises given the critique
        solver_msgs.append(
            {
                "role": "user",
                "content": (
                    "A reviewer raised the following issues. Fix them and output the full "
                    f"corrected solution again in the required format.\n\n{critique}"
                ),
            }
        )
        answer = chat(model, solver_msgs, temperature=temperature)
        solver_msgs.append({"role": "assistant", "content": answer})

    return answer


def escalate(problem_text, spec, ladder=None, log=None, status_out=None):
    """Run the full ladder small->large, threading each layer's answer upward.
    `status_out` is accepted for a uniform SOLVE() signature (populated with the top
    layer's finish_reason)."""
    log = log or (lambda *a, **k: None)
    ladder = ladder or LADDER
    prior = None
    for model in ladder:
        log(f"  layer {model}")
        prior = solve_layer(model, problem_text, spec, prior_answer=prior, log=log)
    if status_out is not None:
        status_out.setdefault("finish_reason", None)
    return prior
