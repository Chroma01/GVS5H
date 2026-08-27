import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = int(next(it))
    groups = [[], [], []]
    totals = [0, 0, 0]
    for _ in range(N):
        v = int(next(it)) - 1
        a = int(next(it))
        c = int(next(it))
        groups[v].append((c, a))
        totals[v] += a

    # If any vitamin is missing entirely, the minimum is 0.
    if min(totals) == 0:
        print(0)
        return

    import numpy as np
    NEG = -(1 << 30)

    def min_cost(items, T, budget):
        # Minimum calories to obtain at least T units from this group.
        # dp[c] = max (capped) value achievable with exactly c calories.
        if budget < 0:
            return None
        dp = np.full(budget + 1, NEG, dtype=np.int64)
        dp[0] = 0
        for c, a in items:
            if a > T:
                a = T
            if c > budget:
                continue
            prev = dp[:-c] + a
            np.maximum(dp[c:], prev, out=dp[c:])
            np.minimum(dp, T, out=dp)
        reach = dp >= T
        if not reach.any():
            return None
        return int(np.argmax(reach))

    def feasible(T):
        rem = X
        for g in groups:
            cost = min_cost(g, T, rem)
            if cost is None:
                return False
            rem -= cost
        return True

    lo, hi = 0, min(totals) + 1  # lo feasible, hi infeasible
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    print(lo)

solve()