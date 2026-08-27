import sys
from itertools import product

# ---------- DP solution under test ----------

def dp_solve(A):
    N = len(A)
    comp = []
    free = 0
    i = 0
    while i < N:
        j = i
        while j < N and A[j] == A[i]:
            j += 1
        free += (j - i - 1)
        comp.append(A[i])
        i = j

    M = len(comp)
    vals = sorted(set(comp))
    vmap = {v: k for k, v in enumerate(vals)}
    B = [vmap[v] for v in comp]

    dp = [0] * (M + 1)
    best = {}
    for i in range(1, M + 1):
        v = B[i - 1]
        cand = dp[i - 1] + 1
        if v in best:
            cand = min(cand, best[v] + i - 1)
        dp[i] = cand
        cur = dp[i] - i
        if v not in best or cur < best[v]:
            best[v] = cur
    return free + dp[M]

# ---------- Brute force over round-label assignments ----------

def brute(A):
    """Min over labelings r[0..n-1] (r_i = r_j => A_i = A_j) of
    (#distinct labels) + (#inversions). Labels normalized to 1..k."""
    n = len(A)
    if n == 0:
        return 0
    best = [float('inf')]

    def rec(i, labels, maxlab):
        if i == n:
            inv = 0
            for x in range(n):
                for y in range(x + 1, n):
                    if labels[x] > labels[y]:
                        inv += 1
            cost = maxlab + inv
            if cost < best[0]:
                best[0] = cost
            return
        # prune: even with 0 future inversions cost can't beat best
        if maxlab >= best[0]:
            return
        for lab in range(1, maxlab + 2):
            # same label => same value: check consistency
            ok = True
            for j in range(i):
                if labels[j] == lab and A[j] != A[i]:
                    ok = False
                    break
            if not ok:
                continue
            labels.append(lab)
            rec(i + 1, labels, max(maxlab, lab))
            labels.pop()

    rec(0, [], 0)
    return best[0]

# ---------- Direct simulation brute force (independent model check) ----------

def brute_ops(A):
    """BFS over actual sequences with the two operations (small n only)."""
    from collections import deque
    start = tuple(A)
    if not start:
        return 0
    dist = {start: 0}
    dq = deque([start])
    while dq:
        s = dq.popleft()
        d = dist[s]
        K = len(s)
        # swaps
        for i in range(K - 1):
            t = list(s)
            t[i], t[i + 1] = t[i + 1], t[i]
            t = tuple(t)
            if t not in dist:
                dist[t] = d + 1
                dq.append(t)
        # deletions of equal prefix
        i = 0
        while i < K and s[i] == s[0]:
            i += 1
            t = s[i:]
            if t not in dist:
                dist[t] = d + 1
                if not t:
                    return d + 1
                dq.append(t)
    return dist[()]

# ---------- Tests ----------

def run_tests():
    # 1) Sample checks
    assert dp_solve([1, 1, 2, 1, 2]) == 3, dp_solve([1, 1, 2, 1, 2])
    assert dp_solve([4, 2, 1, 3]) == 4
    assert dp_solve([1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]) == 8

    # 2) Edge cases
    assert dp_solve([7] * 10) == 1          # all equal -> 1
    assert dp_solve(list(range(1, 9))) == 8  # all distinct -> N
    assert dp_solve([1, 1]) == 1
    assert dp_solve([1, 2]) == 2
    assert dp_solve([2, 2, 2]) == 1

    # 3) Exhaustive: all sequences length <= 7 over {1,2,3}, DP vs label-brute
    for n in range(1, 8):
        for A in product((1, 2, 3), repeat=n):
            d = dp_solve(list(A))
            b = brute(list(A))
            assert d == b, (A, d, b)

    # 4) Cross-check label-brute vs operation-BFS on small sequences
    for n in range(1, 7):
        for A in product((1, 2), repeat=n):
            b1 = brute(list(A))
            b2 = brute_ops(list(A))
            assert b1 == b2, (A, b1, b2)
    for n in range(1, 6):
        for A in product((1, 2, 3), repeat=n):
            b1 = brute(list(A))
            b2 = brute_ops(list(A))
            assert b1 == b2, (A, b1, b2)

    print("ALL TESTS PASSED")

run_tests()