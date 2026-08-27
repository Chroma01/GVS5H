"""Multi-agent collaborative solver: a primary "manager" plus worker subagents,
coordinating over a SHARED FILESYSTEM WORKSPACE. Emulates the Claude-Code
orchestrator/subagent pattern, but every role is the SAME model
(default groq:qwen/qwen3.6-27b) invoked in a fresh context.

Control flow (as requested):
  1. PRIMARY writes an overarching plan and seeds the task list.
  2. The FIRST WORKER just thinks about the problem and proposes approaches.
  3. Loop: PRIMARY decides which task to prioritize and spawns a worker; the
     worker completes it, updates the shared code/proof, and proposes next steps.
     Primary stops when it judges the problem solved (or the iteration budget
     runs out).
  4. A FINALIZE worker emits the definitive artifact, which is then graded.

Shared workspace (real files, so every role sees the same evolving state):
    <ws>/task.md      the problem statement
    <ws>/plan.md      the primary's overarching plan
    <ws>/tasks.json   the task list [{id, desc, status, result}]
    <ws>/notes.md     accumulated ideas / proofs / findings
    <ws>/solution.py  current best code   (code problems)
    <ws>/answer.md    current best answer  (math problems)
"""

import os
import re
import time
import json
import hashlib

from orchestrator import chat  # groq:/ollama dispatch

MODEL = os.environ.get("MULTIAGENT_MODEL", "groq:qwen/qwen3.6-27b")
MAX_ITERS = int(os.environ.get("MULTIAGENT_MAX_ITERS", "4"))   # primary->worker cycles
MAX_TASKS = int(os.environ.get("MULTIAGENT_MAX_TASKS", "12"))  # cap on live task list
WS_ROOT = os.environ.get("MULTIAGENT_WS", os.path.join(os.path.dirname(os.path.abspath(__file__)), "ws"))


# --- workspace helpers -----------------------------------------------------

def _slug(text):
    return hashlib.md5(text.encode()).hexdigest()[:12]


def _read(ws, name):
    p = os.path.join(ws, name)
    return open(p).read() if os.path.exists(p) else ""


def _write(ws, name, content):
    with open(os.path.join(ws, name), "w") as f:
        f.write(content)


def _append(ws, name, content):
    with open(os.path.join(ws, name), "a") as f:
        f.write(content)


# --- transcript logging ----------------------------------------------------
# Every agent call for a problem is appended to <ws>/transcript.jsonl: the first
# line is a _meta record, then one record per call {role, request, response}.

def _record(ws, rec):
    with open(os.path.join(ws, "transcript.jsonl"), "a") as f:
        f.write(json.dumps(rec) + "\n")


def _chat(ws, role, messages, temperature, meta=None):
    """Model call that also transcripts the full request/response for this problem.
    If `meta` is passed it is populated with {finish_reason, completion_tokens}."""
    m = meta if meta is not None else {}
    resp = chat(MODEL, messages, temperature=temperature, meta=m)
    _record(ws, {"t": time.time(), "role": role, "request": messages, "response": resp,
                 "finish_reason": m.get("finish_reason"), "completion_tokens": m.get("completion_tokens")})
    return resp


# --- parsing helpers -------------------------------------------------------

def _strip_think(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def _sections(text):
    """Split a model reply into {HEADER: body}. Accepts '### H', '**H**', 'H:'."""
    out, cur, buf = {}, None, []
    for line in _strip_think(text).splitlines():
        s = line.strip()
        m = (re.match(r"^#{1,3}\s*([A-Za-z_]+)\s*$", s)
             or re.match(r"^\*\*([A-Za-z_]+)\*\*\s*:?\s*$", s)
             or re.match(r"^([A-Z_]{3,})\s*:\s*$", s))
        if m:
            if cur is not None:
                out[cur] = "\n".join(buf).strip()
            cur, buf = m.group(1).upper(), []
        else:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf).strip()
    return out


def _bullets(text):
    items = []
    for line in text.splitlines():
        m = re.match(r"^\s*(?:[-*]|\d+[.)])\s+(.*\S)", line)
        if m:
            items.append(m.group(1).strip())
    return items


def _extract_py(text):
    m = re.search(r"```(?:python)?\s*\n(.*?)```", _strip_think(text), re.DOTALL)
    return m.group(1).strip() if m else ""


def _parse_tasks(text):
    """Parse the primary's curated list: lines like '- [done] ...' / '- [todo] ...'."""
    out = []
    for b in _bullets(text):
        m = re.match(r"\[\s*([a-z_ ]+?)\s*\]\s*(.*)", b, re.I)
        if m:
            raw = m.group(1).lower().replace(" ", "").replace("_", "")
            desc = m.group(2).strip()
            status = "done" if raw == "done" else ("in_progress" if raw in ("wip", "inprogress") else "pending")
        else:
            desc, status = b, "pending"
        if desc:
            out.append({"id": len(out) + 1, "desc": desc, "status": status, "result": ""})
    return out[:MAX_TASKS]


ANS_RE = re.compile(r"ANSWER:\s*\S", re.I)  # any non-empty final answer (int or expression)
# A genuine final answer is short. Anything longer is a reasoning dump, not an answer.
MAX_ANSWER_CHARS = 20000


def _has_answer(ws, spec):
    """True if the workspace already holds a usable final artifact."""
    if spec["kind"] == "code":
        return bool(_read(ws, "solution.py").strip())
    return bool(ANS_RE.search(_read(ws, "answer.md")))


# --- roles -----------------------------------------------------------------

def _save_tasks(ws, tasks):
    _write(ws, "tasks.json", json.dumps(tasks, indent=2))


def _add_tasks(tasks, descs):
    have = {t["desc"].lower() for t in tasks}
    nid = max([t["id"] for t in tasks], default=0)
    for d in descs:
        d = d.strip()
        if d and d.lower() not in have and len(tasks) < MAX_TASKS:
            nid += 1
            tasks.append({"id": nid, "desc": d, "status": "pending", "result": ""})
            have.add(d.lower())


def _primary_plan(problem, spec, ws, log):
    kind = spec["kind"]
    sys = (
        "You are the PRIMARY orchestrator (manager) of a small team of workers, all "
        f"expert at {'competitive programming' if kind == 'code' else 'olympiad mathematics'}. "
        "Given a problem, produce a short overarching plan to solve it, then a task list "
        "the workers can pick up. Respond with EXACTLY these sections:\n"
        "### PLAN\n<3-6 sentence strategy>\n"
        "### TASKS\n<3-6 bullet tasks, each a concrete unit of work>"
    )
    reply = _chat(ws, "primary_plan", [
        {"role": "system", "content": sys},
        {"role": "user", "content": problem},
    ], temperature=0.3)
    sec = _sections(reply)
    _write(ws, "plan.md", sec.get("PLAN", reply.strip()))
    tasks = []
    _add_tasks(tasks, _bullets(sec.get("TASKS", "")))
    log(f"    [primary] plan + {len(tasks)} initial tasks")
    return tasks


def _ideation_worker(problem, spec, ws, log):
    """First worker: think about the problem and PROPOSE approaches (returns a list).
    Its proposals are folded into the task list by the primary, not appended blindly."""
    sys = (
        "You are the FIRST WORKER. Do NOT solve the problem yet. Just think about it: "
        "identify the core difficulty, list candidate approaches, and note pitfalls. "
        "Respond with EXACTLY:\n### NOTES\n<your analysis>\n"
        "### NEXT\n<bullet list of concrete approaches/tasks to try next>"
    )
    reply = _chat(ws, "ideation", [
        {"role": "system", "content": sys},
        {"role": "user", "content": f"PROBLEM:\n{problem}\n\nPLAN:\n{_read(ws, 'plan.md')}"},
    ], temperature=0.4)
    sec = _sections(reply)
    _append(ws, "notes.md", f"\n## ideation\n{sec.get('NOTES', reply.strip())}\n")
    proposals = _bullets(sec.get("NEXT", ""))
    log(f"    [worker:ideate] proposed {len(proposals)} approaches")
    return proposals


def _primary_manage(problem, spec, ws, tasks, proposals, last_summary, log):
    """Primary monitors progress, curates the task list, and decides done/next.

    Reviews the current solution + the latest worker's result, then rewrites the task
    list (merge duplicates, mark done, fold in only genuinely new proposals) and either
    declares the problem solved or names the single next task.
    Returns (status, next_desc, curated_tasks).
    """
    kind = spec["kind"]
    cur = _read(ws, "solution.py" if kind == "code" else "answer.md").strip()
    task_lines = "\n".join(
        f"- [{'done' if t['status'] == 'done' else 'todo'}] {t['desc']}" for t in tasks
    ) or "(none)"
    prop_lines = "\n".join(f"- {p}" for p in proposals) or "(none)"
    sys = (
        "You are the PRIMARY orchestrator and manager. You OWN the task list and decide "
        "when the problem is solved. Review the current progress and the latest worker's "
        "result, then:\n"
        "- If the current solution/answer is complete and correct, set STATUS to 'done'.\n"
        "- Otherwise CURATE the task list: merge duplicates, drop finished or irrelevant "
        "items, mark completed ones [done], and fold in ONLY genuinely new sub-tasks from "
        "the proposals. Then choose the single most valuable next task.\n"
        "Respond with EXACTLY these sections:\n"
        "### STATUS\n<done|continue>\n"
        "### NEXT\n<exact text of the ONE task to do next; omit if done>\n"
        "### TASKS\n<curated list, one per line, each '- [done] ...' or '- [todo] ...'>"
    )
    reply = _chat(ws, "primary_manage", [
        {"role": "system", "content": sys},
        {"role": "user", "content": (
            f"PROBLEM:\n{problem}\n\nCURRENT {'SOLUTION' if kind == 'code' else 'ANSWER'}:\n"
            f"{cur or '(none yet)'}\n\nNOTES:\n{_read(ws, 'notes.md')}\n\n"
            f"CURRENT TASK LIST:\n{task_lines}\n\nLATEST WORKER RESULT: {last_summary}\n\n"
            f"PROPOSED NEW STEPS:\n{prop_lines}"
        )},
    ], temperature=0.2)
    sec = _sections(reply)
    curated = _parse_tasks(sec.get("TASKS", "")) or tasks
    status = "done" if sec.get("STATUS", "").strip().lower().startswith("done") else "continue"
    if status == "done" and not cur:  # invariant: can't be done with no answer produced yet
        status = "continue"
    nxt = (_bullets(sec.get("NEXT", ""))[:1] or [sec.get("NEXT", "").strip()])[0]
    nxt = re.sub(r"^[-*]\s*", "", nxt).strip()
    if status == "continue" and not nxt:  # manager wants to continue but named no task
        todo = [t for t in curated if t["status"] != "done"]
        nxt = todo[0]["desc"] if todo else ""
    log(f"    [primary-manage] {status}" + (f", next: {nxt[:60]}" if status == "continue" else ""))
    return status, nxt, curated


def _worker(problem, spec, ws, task, log, finalize=False):
    kind = spec["kind"]
    cur = _read(ws, "solution.py" if kind == "code" else "answer.md")
    if kind == "code":
        out_fmt = (
            "### CODE\n```python\n<the FULL updated self-contained program>\n```\n"
            "### NOTES\n<what you did / any proof or reasoning>\n"
            "### NEXT\n<bullet list of remaining steps, or 'none'>\n### STATUS\n<solved|continue>"
        )
    else:
        out_fmt = (
            "### ANSWER\n<full worked solution, ending with the exact final "
            "ANSWER: line your instructions require>\n"
            "### NOTES\n<key steps / proof>\n"
            "### NEXT\n<bullet list of remaining checks, or 'none'>\n### STATUS\n<solved|continue>"
        )
    goal = (
        "Produce the DEFINITIVE final solution now, using all notes and current work."
        if finalize else f"Complete this task: {task['desc']}"
    )
    sys = (
        f"You are a WORKER subagent, {spec['solver_system']} "
        "You share a workspace with the team. Build on the current work and notes. "
        f"Respond with EXACTLY these sections:\n{out_fmt}"
    )
    reply = _chat(ws, "finalize" if finalize else f"worker:{task['id']}", [
        {"role": "system", "content": sys},
        {"role": "user", "content": (
            f"PROBLEM:\n{problem}\n\nPLAN:\n{_read(ws, 'plan.md')}\n\n"
            f"NOTES:\n{_read(ws, 'notes.md')}\n\nCURRENT WORK:\n{cur or '(none yet)'}\n\n"
            f"YOUR TASK: {goal}"
        )},
    ], temperature=0.2)
    sec = _sections(reply)
    if kind == "code":
        code = _extract_py(sec.get("CODE", "")) or _extract_py(reply)
        if code:
            _write(ws, "solution.py", code)
    else:
        ans = sec.get("ANSWER", "").strip()
        if not ans and ANS_RE.search(reply) and len(reply) < MAX_ANSWER_CHARS:
            # No '### ANSWER' header, but a short reply that does state a final answer.
            ans = _strip_think(reply).strip()
        # A reply with neither the section nor a short final answer is a failed or truncated
        # call. Writing its raw text here is what let a 100k-char reasoning dump become the
        # workspace's "current answer", which the manager could never make progress against.
        # Only overwrite if this response has a parseable final answer (or there is
        # nothing yet): a rambling/truncated call must not destroy a good prior answer.
        if ans and (ANS_RE.search(ans) or not _read(ws, "answer.md").strip()):
            _write(ws, "answer.md", ans)
    if sec.get("NOTES"):
        _append(ws, "notes.md", f"\n## worker: {task['desc'][:50]}\n{sec['NOTES']}\n")
    nexts = [b for b in _bullets(sec.get("NEXT", "")) if b.lower() != "none"]
    status = sec.get("STATUS", "continue").strip().lower()
    summary = f"worker reported '{status}' on: {task['desc'][:80]}. " + (sec.get("NOTES", "")[:200])
    log(f"    [worker] task {task['id']} -> {status}, +{len(nexts)} next steps")
    return status, nexts, summary


# --- public entry point ----------------------------------------------------

def multiagent_solve(problem_text, spec, log=None, status_out=None):
    """Same signature as escalate(): returns final answer text for grading.
    If `status_out` is passed, it gets the last call's finish_reason plus a count of
    truncated (finish_reason=length) calls over the whole problem."""
    log = log or (lambda *a, **k: None)
    ws = os.path.join(WS_ROOT, _slug(problem_text))
    os.makedirs(ws, exist_ok=True)
    _write(ws, "task.md", problem_text)
    _write(ws, "notes.md", "")
    _write(ws, "transcript.jsonl", "")  # fresh transcript per run
    _record(ws, {"_meta": True, "t": time.time(), "model": MODEL,
                 "kind": spec["kind"], "max_iters": MAX_ITERS, "problem": problem_text})

    tasks = _primary_plan(problem_text, spec, ws, log)
    proposals = _ideation_worker(problem_text, spec, ws, log)
    # Primary folds the plan + ideation into one curated list and picks the first task.
    status, next_desc, tasks = _primary_manage(
        problem_text, spec, ws, tasks, proposals, "ideation complete", log)
    _save_tasks(ws, tasks)

    # Primary manages the loop: worker does the chosen task, then the primary reviews
    # progress, re-curates the list, and decides whether the problem is done.
    iters, prev_desc = 0, None
    while status == "continue" and next_desc and iters < MAX_ITERS:
        # No-progress guard: if the manager hands back the very same task it just assigned,
        # the worker achieved nothing and another identical cycle will too. Each cycle can
        # cost a full CLOUD_MAX_TOKENS generation, so stop rather than spend the budget.
        if prev_desc is not None and next_desc.strip().lower() == prev_desc.strip().lower():
            log(f"    [primary] reissued the same task; no progress, stopping after {iters} iters")
            break
        prev_desc = next_desc
        iters += 1
        task = {"id": iters, "desc": next_desc, "status": "in_progress", "result": ""}
        _, nexts, summary = _worker(problem_text, spec, ws, task, log)
        status, next_desc, tasks = _primary_manage(
            problem_text, spec, ws, tasks, nexts, summary, log)
        _save_tasks(ws, tasks)

    # Finalize only if the primary didn't already sign off on a usable answer (a redundant
    # finalize can ramble past the token cap and destroy a correct intermediate answer).
    if status == "done" and _has_answer(ws, spec):
        log("    [finalize] skipped (primary marked done)")
    else:
        _worker(problem_text, spec, ws, {"id": 0, "desc": "finalize"}, log, finalize=True)

    if status_out is not None:
        # summarize call outcomes across the whole problem from the transcript
        recs = []
        for ln in open(os.path.join(ws, "transcript.jsonl")):
            r = json.loads(ln)
            if not r.get("_meta"):
                recs.append(r)
        status_out["finish_reason"] = recs[-1].get("finish_reason") if recs else None
        status_out["truncated_calls"] = sum(1 for r in recs if r.get("finish_reason") == "length")
        status_out["n_calls"] = len(recs)

    if spec["kind"] == "code":
        code = _read(ws, "solution.py")
        return f"```python\n{code}\n```" if code else ""
    return _read(ws, "answer.md")


def single_solve(problem_text, spec, log=None, status_out=None):
    """Single-shot baseline: one model call, no orchestration. Same signature as
    escalate()/multiagent_solve(); transcripts each problem like the multi-agent path.
    If `status_out` (a dict) is passed, it gets {finish_reason, completion_tokens} of the call."""
    log = log or (lambda *a, **k: None)
    ws = os.path.join(WS_ROOT, _slug(problem_text))
    os.makedirs(ws, exist_ok=True)
    _write(ws, "task.md", problem_text)
    _write(ws, "transcript.jsonl", "")
    _record(ws, {"_meta": True, "t": time.time(), "model": MODEL,
                 "kind": spec["kind"], "engine": "single", "problem": problem_text})
    meta = {}
    answer = _chat(ws, "single", [
        {"role": "system", "content": spec["solver_system"]},
        {"role": "user", "content": problem_text},
    ], temperature=0.2, meta=meta)
    if status_out is not None:
        status_out.update(meta)
    log(f"    [single] {len(answer)} chars  finish={meta.get('finish_reason')}")
    return answer
