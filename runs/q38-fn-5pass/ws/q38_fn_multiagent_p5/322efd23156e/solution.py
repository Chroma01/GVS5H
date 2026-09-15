import sys
from bisect import bisect_left


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    it = iter(data)
    N = next(it)
    X = next(it)

    groups = [[] for _ in range(3)]
    totals = [0, 0, 0]

    for _ in range(N):
        v = next(it)
        a = next(it)
        c = next(it)
        idx = v - 1
        groups[idx].append((c, a))
        totals[idx] += a

    # If some vitamin cannot be obtained at all, the answer is 0.
    if min(totals) == 0:
        print(0)
        return

    dps = []
    rng = range

    for g in groups:
        dp = [0] * (X + 1)

        # 0/1 knapsack for this vitamin type:
        # dp[c] = maximum amount of this vitamin with at most c calories.
        for w, val in g:
            for cap in rng(X, w - 1, -1):
                nv = dp[cap - w] + val
                if nv > dp[cap]:
                    dp[cap] = nv

        # Ensure nondecreasing "at most c calories" semantics.
        for cap in rng(1, X + 1):
            if dp[cap] < dp[cap - 1]:
                dp[cap] = dp[cap - 1]

        dps.append(dp)

    def feasible(t):
        need = 0
        for dp in dps:
            c = bisect_left(dp, t)
            if c > X:
                return False
            need += c
            if need > X:
                return False
        return True

    low = 0
    high = min(totals) + 1

    while high - low > 1:
        mid = (low + high) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid

    print(low)


if __name__ == "__main__":
    solve()