#!/usr/bin/env python3
"""Re-grade stored generations against the CURRENT evaluator, without re-running any model.

Why this exists: LiveCodeBench's stdin mock had a stateless `MockBuffer.readline()` that
returned line 1 on every call (lcb_runner/evaluation/testing_util.py). Any solution reading
multi-line input via `sys.stdin.buffer.readline()` therefore scored wrong no matter how
correct it was -- while the v2 scaffold's sample verifier, which runs the candidate as a real
subprocess, saw it pass. The two disagreed, and the manager was told "correct" for programs
the grader rejected. This regrades the existing `code` fields so the fix can be measured
against the numbers it replaces.

    uv run --project /home/persis/model-test python escalation/regrade.py <results.json> ...

Writes <name>.regraded.json beside each input and prints an old-vs-new summary. Inputs are
never modified.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "LiveCodeBench"))

from lcb_runner.benchmarks.code_generation import load_code_generation_dataset
from lcb_runner.evaluation.compute_code_generation_metrics import codegen_metrics

import numpy as np


def _passed(res0):
    """Same rule run_bench.py uses: every test must be > 0, and there must be tests."""
    if isinstance(res0, (list, tuple)):
        return bool(np.all(np.array(res0) > 0)) and len(res0) > 0
    return bool(res0)


def regrade_all(paths, problems):
    """Grade every record of every file in ONE evaluator call.

    Grading one file at a time is what makes this slow, and the reason is not the pool
    size. check_correctness() runs a problem's whole test suite in a single child process
    and the pool worker then blocks in p.join() for up to 7*n_tests+5 seconds, burning no
    CPU. A file's ~100 problems finish in seconds except two or three slow or looping ones,
    so most of each file's wall clock is idle workers waiting on that tail -- and grading
    62 files sequentially pays the tail 62 times. Pooling every file into one call lets the
    tails of different files overlap, which is what actually keeps the cores busy.
    """
    # Some files in the older run directories are placeholders rather than results: the
    # 128k opus_single cell is {"skipped": ...} and the nemotron files are {"note": ...}.
    # They carry no records, so they are dropped here with a line rather than crashing the
    # whole batch on a KeyError.
    kept = []
    for path in paths:
        blob = json.load(open(path))
        if "lcb" not in blob or not blob["lcb"].get("records"):
            print(f"  skip (no records): {os.path.basename(path)}")
            continue
        kept.append((path, blob))
    paths = [p for p, _ in kept]

    blobs, index = [], []          # index: (blob_i, record_i) per graded generation
    samples, generations = [], []
    for bi, (path, blob) in enumerate(kept):
        blobs.append(blob)
        for ri, r in enumerate(blob["lcb"]["records"]):
            # A record with no code is failed here rather than sent to the evaluator, which
            # would score "" wrong anyway and only costs a process slot. Writing the fail
            # matters: skipping the record would leave whatever `passed` the source file
            # carried, and for the cap-matched arm that is a pass earned by the untruncated
            # generation whose code the 128k cut removed (escalation/capmatch_q38.py).
            if not (r.get("code") or "").strip():
                r["passed_before_regrade"] = bool(r.get("passed"))
                r["passed"] = False
                continue
            qid = r["question_id"]
            if qid not in problems:
                raise SystemExit(f"{path}: id {qid!r} is not in the loaded dataset")
            index.append((bi, ri))
            samples.append(problems[qid].get_evaluation_sample())
            generations.append([r["code"]])

    nproc = int(os.environ.get("REGRADE_PROCS", min(96, max(8, (os.cpu_count() or 8) // 2))))
    print(f"grading {len(generations)} generations from {len(paths)} files "
          f"with {nproc} workers", flush=True)
    _, results, _ = codegen_metrics(samples, generations, k_list=[1], num_process_evaluate=nproc)

    for n, (bi, ri) in enumerate(index):
        rec = blobs[bi]["lcb"]["records"][ri]
        rec["passed_before_regrade"] = bool(rec.get("passed"))
        rec["passed"] = _passed(results[n][0])

    out = []
    for path, blob in zip(paths, blobs):
        recs = blob["lcb"]["records"]
        graded = [r for r in recs if r.get("status") != "infra"]
        npass = sum(bool(r["passed"]) for r in graded)
        old = blob["lcb"]["pass@1"]
        blob["lcb"]["pass@1_before_regrade"] = old
        blob["lcb"]["pass@1"] = 100.0 * npass / max(1, len(graded))
        dst = path.replace(".json", ".regraded.json")
        json.dump(blob, open(dst, "w"))
        flips = [(r["question_id"], r["passed_before_regrade"], r["passed"])
                 for r in recs if "passed_before_regrade" in r
                 and r["passed_before_regrade"] != r["passed"]]
        out.append((path, old, blob["lcb"]["pass@1"], flips))
    return out


def main():
    paths = sys.argv[1:]
    if not paths:
        raise SystemExit(__doc__)
    os.environ.setdefault("LCB_RELEASE", "release_v6")
    problems = {p.question_id: p
                for p in load_code_generation_dataset(release_version=os.environ["LCB_RELEASE"])}
    print(f"loaded {len(problems)} problems from {os.environ['LCB_RELEASE']}\n")
    for path, old, new, flips in regrade_all(paths, problems):
        gained = sum(1 for _, w, n in flips if n and not w)
        lost = sum(1 for _, w, n in flips if w and not n)
        # capmatch_q38.py clears pass@1 on the files it writes, so `old` can be absent.
        was = f"{old:5.1f}" if old is not None else "    -"
        print(f"{os.path.basename(path):34} {was} -> {new:5.1f}  "
              f"({gained:+3d} newly passing, {lost:3d} newly failing)")
        for qid, was, now in flips:
            if was and not now:  # a regression is the interesting direction; list those
                print(f"    !! now failing: {qid}")


if __name__ == "__main__":
    main()
