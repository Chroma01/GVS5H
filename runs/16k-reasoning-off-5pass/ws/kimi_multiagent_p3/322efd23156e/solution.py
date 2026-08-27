import sys
import numpy as np

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    X = int(data[idx]); idx += 1

    # Group items by vitamin type (1, 2, 3)
    items = [[], [], []]
    for _ in range(N):
        v = int(data[idx]); a = int(data[idx + 1]); c = int(data[idx + 2])
        idx += 3
        items[v - 1].append((a, c))

    # If any vitamin type is missing entirely, answer is 0
    for g in items:
        if not g:
            print(0)
            return

    # Per-vitamin 0/1 knapsack: dp[c] = max vitamin value achievable
    # with total calories <= c (after accumulate). Computed once.
    frontiers = []
    totals = []
    for g in items:
        dp = np.full(X + 1, -(1 << 60), dtype=np.int64)
        dp[0] = 0
        for a, c in g:
            # 0/1 knapsack update; RHS creates temp arrays so no item reuse
            dp[c:] = np.maximum(dp[c:], dp[:-c] + a)
        np.maximum.accumulate(dp, out=dp)  # now dp[c] = best with at most c calories
        frontiers.append(dp)
        totals.append(int(dp[X]))

    # Upper bound for binary search: scarcest vitamin's total
    hi = min(totals)
    lo = 0

    # Maximize T such that sum of min calories to reach T of each vitamin <= X
    while lo < hi:
        mid = (lo + hi + 1) // 2
        total_cal = 0
        ok = True
        for dp in frontiers:
            c = int(np.searchsorted(dp, mid))
            if c > X:
                ok = False
                break
            total_cal += c
            if total_cal > X:
                ok = False
                break
        if ok:
            lo = mid
        else:
            hi = mid - 1

    print(lo)

main()