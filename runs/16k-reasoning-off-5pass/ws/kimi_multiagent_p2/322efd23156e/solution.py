import sys
import numpy as np

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); X = int(data[1])
    groups = [[], [], []]
    idx = 2
    for _ in range(n):
        v = int(data[idx]) - 1
        a = int(data[idx + 1])
        c = int(data[idx + 2])
        idx += 3
        groups[v].append((a, c))

    NEG = -10**18
    bests = []
    for g in groups:
        dp = np.full(X + 1, NEG, dtype=np.int64)
        dp[0] = 0
        for a, c in g:
            # 0/1 knapsack: numpy evaluates the entire RHS into temporary
            # arrays before the in-place slice assignment, so each item is
            # used at most once (equivalent to iterating calories descending).
            dp[c:] = np.maximum(dp[c:], dp[:-c] + a)
        # best[c] = max value obtainable with at most c calories
        bests.append(np.maximum.accumulate(dp))

    b1, b2, b3 = bests
    b1l = b1.tolist()
    b2l = b2.tolist()
    b3l = b3.tolist()

    ans = 0
    for c1 in range(X + 1):
        v1 = b1l[c1]
        if v1 <= ans:
            continue
        R = X - c1
        lo, hi = 0, R
        # f(c2) = min(b2[c2], b3[R - c2]) is unimodal (non-decreasing then
        # non-increasing): b2[c2] is non-decreasing in c2, b3[R-c2] is
        # non-increasing in c2. Ternary search over the integer domain,
        # then scan the small remaining window exactly.
        while hi - lo > 3:
            m1 = lo + (hi - lo) // 3
            m2 = hi - (hi - lo) // 3
            f1 = min(b2l[m1], b3l[R - m1])
            f2 = min(b2l[m2], b3l[R - m2])
            if f1 < f2:
                lo = m1
            else:
                hi = m2
        best23 = NEG
        for c2 in range(lo, hi + 1):
            val = min(b2l[c2], b3l[R - c2])
            if val > best23:
                best23 = val
        cand = min(v1, best23)
        if cand > ans:
            ans = cand
    print(max(ans, 0))

main()