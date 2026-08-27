import sys
from collections import deque
from functools import lru_cache


def main():
    data = sys.stdin.read().split()
    # RESEARCH/BRUTE-FORCE harness (not the final solution).
    # Exhaustively checks candidate feasibility predicates against true
    # BFS reachability for tiny N, and prints the analysis requested:
    #  (a) pred3 mismatch count (validates assignment framework),
    #  (b) pred2 k>=2 FP/FN counts + samples (is obstruction k=1-only?),
    #  (c) true min k for {1,3,5}->{1,3,4},
    #  (d) final predicate verification (zero mismatches expected).

    out = []

    def step(mask, i, n):
        nm = 0
        for j in range(1, n + 1):
            if mask >> (j - 1) & 1:
                if j < i:
                    nj = j + 1
                elif j > i:
                    nj = j - 1
                else:
                    nj = j
                nm |= 1 << (nj - 1)
        return nm

    def reachable_in_k(start, k, n):
        dist = {start: 0}
        dq = deque([start])
        while dq:
            m = dq.popleft()
            d = dist[m]
            if d == k:
                continue
            for i in range(1, n + 1):
                nm = step(m, i, n)
                if nm not in dist:
                    dist[nm] = d + 1
                    dq.append(nm)
        return dist

    def positions(mask, n):
        return [j for j in range(1, n + 1) if mask >> (j - 1) & 1]

    # ---- candidate predicates ----

    def pred_assignment(P, Q, k):
        # exists nondecreasing surjection pieces->targets, |disp| <= k
        np_, nq = len(P), len(Q)

        @lru_cache(maxsize=None)
        def go(pi, qi):
            if pi == np_:
                return qi == nq
            res = False
            if qi > 0 and abs(P[pi] - Q[qi - 1]) <= k:      # merge onto prev
                res = res or go(pi + 1, qi)
            if qi < nq and abs(P[pi] - Q[qi]) <= k:         # cover next
                res = res or go(pi + 1, qi + 1)
            return res
        return go(0, 0)

    def all_assignments(P, Q, k):
        np_, nq = len(P), len(Q)
        maps, cur = [], []

        def rec(pi, last, covered):
            if pi == np_:
                if covered == (1 << nq) - 1:
                    maps.append(tuple(cur))
                return
            for qj in range(last, nq):
                if abs(P[pi] - Q[qj]) <= k:
                    cur.append(qj)
                    rec(pi + 1, qj, covered | (1 << qj))
                    cur.pop()
        rec(0, 0, 0)
        return maps

    def k1_consistent(P, Q):
        # k == 1: single target i must realize everything in one step.
        for am in all_assignments(P, Q, 1):
            stay = set()
            for pi, qj in enumerate(am):
                if Q[qj] == P[pi]:
                    stay.add(P[pi])
            if len(stay) > 1:
                continue
            if len(stay) == 1:
                s = next(iter(stay))
                good = True
                for pi, qj in enumerate(am):
                    d = Q[qj] - P[pi]
                    if d > 0 and not (P[pi] < s):
                        good = False
                    if d < 0 and not (P[pi] > s):
                        good = False
                if good:
                    return True
            else:
                maxr, minl = -1, 10 ** 9
                for pi, qj in enumerate(am):
                    d = Q[qj] - P[pi]
                    if d > 0:
                        maxr = max(maxr, P[pi])
                    if d < 0:
                        minl = min(minl, P[pi])
                if maxr < minl:
                    return True
        return False

    def pred2(P, Q, k):
        # hypothesis: k==0 -> equality; k==1 -> single-target rule;
        #             k>=2 -> plain assignment (under test)
        if k == 0:
            return P == Q
        if k == 1:
            return k1_consistent(P, Q)
        return pred_assignment(P, Q, k)

    def feasible_assignment(P, Q, am, k, n):
        # exact: can pieces follow the fixed assignment in exactly k steps?
        start = tuple(P)
        goal = tuple(Q[qj] for qj in am)
        cur = {start}
        for _ in range(k):
            nxt = set()
            for state in cur:
                for i in range(1, n + 1):
                    ns = tuple(p + 1 if p < i else (p - 1 if p > i else p)
                               for p in state)
                    nxt.add(ns)
            cur = nxt
        return goal in cur

    def pred3(P, Q, k, n):
        # exists assignment realizable in exactly k steps (exact check)
        if k == 0:
            return P == Q
        for am in all_assignments(P, Q, k):
            if feasible_assignment(P, Q, am, k, n):
                return True
        return False

    # ---- exhaustive comparison ----
    KMAX = 4
    mism1, mism2, mism3 = [], [], []
    for n in range(1, 6):
        allm = list(range(1, 1 << n))
        for s in allm:
            P = positions(s, n)
            dist = reachable_in_k(s, KMAX, n)
            for t in allm:
                Q = positions(t, n)
                for k in range(0, KMAX + 1):
                    truth = t in dist and dist[t] <= k
                    if pred_assignment(P, Q, k) != truth:
                        mism1.append((n, P, Q, k, truth))
                    if pred2(P, Q, k) != truth:
                        mism2.append((n, P, Q, k, truth))
                    if pred3(P, Q, k, n) != truth:
                        mism3.append((n, P, Q, k, truth))

    out.append(f"(a) pred3 (exact per-assignment) mismatches: {len(mism3)}")
    for m in mism3[:20]:
        out.append("    n={} P={} Q={} k={} truth={}".format(*m))

    out.append(f"pred1 (plain assignment, all k) mismatches: {len(mism1)}")
    fp1 = [m for m in mism1 if m[4] is False]
    fn1 = [m for m in mism1 if m[4] is True]
    out.append(f"  pred1 false-positives: {len(fp1)}, false-negatives: {len(fn1)}")
    for m in fp1[:10]:
        out.append("    FP n={} P={} Q={} k={}".format(m[0], m[1], m[2], m[3]))
    for m in fn1[:10]:
        out.append("    FN n={} P={} Q={} k={}".format(m[0], m[1], m[2], m[3]))

    fp2 = [m for m in mism2 if m[3] >= 2 and m[4] is False]
    fn2 = [m for m in mism2 if m[3] >= 2 and m[4] is True]
    out.append(f"(b) pred2 k>=2 false-positives: {len(fp2)}")
    for m in fp2[:40]:
        out.append("    FP n={} P={} Q={} k={}".format(m[0], m[1], m[2], m[3]))
    out.append(f"    pred2 k>=2 false-negatives: {len(fn2)}")
    for m in fn2[:40]:
        out.append("    FN n={} P={} Q={} k={}".format(m[0], m[1], m[2], m[3]))
    out.append(f"    pred2 total mismatches (incl k=0,1): {len(mism2)}")
    for m in mism2[:20]:
        out.append("    n={} P={} Q={} k={} truth={}".format(*m))

    # (c) counterexample min k
    n = 5
    s = sum(1 << (x - 1) for x in [1, 3, 5])
    t = sum(1 << (x - 1) for x in [1, 3, 4])
    dist = reachable_in_k(s, 8, n)
    out.append(f"(c) {{1,3,5}}->{{1,3,4}}: min k = {dist.get(t, 'unreachable<=8')}")

    # (d) final predicate re-verification (identical to pred2, stated cleanly)
    def final_pred(P, Q, k):
        if k == 0:
            return P == Q
        if k == 1:
            return k1_consistent(P, Q)
        return pred_assignment(P, Q, k)

    bad = 0
    for n in range(1, 6):
        allm = list(range(1, 1 << n))
        for s in allm:
            P = positions(s, n)
            dist = reachable_in_k(s, KMAX, n)
            for t in allm:
                Q = positions(t, n)
                for k in range(0, KMAX + 1):
                    truth = t in dist and dist[t] <= k
                    if final_pred(P, Q, k) != truth:
                        bad += 1
    out.append(f"(d) final predicate mismatches on n<=5, k<=4: {bad}")

    print("\n".join(out))


main()