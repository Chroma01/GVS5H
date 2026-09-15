import sys
from bisect import bisect_left


def build_dp(items, X):
    by_c = {}
    for c, a in items:
        if c <= X:
            if c in by_c:
                by_c[c].append(a)
            else:
                by_c[c] = [a]

    if not by_c:
        return [0] * (X + 1)

    # For items with the same calorie cost, only the best X // c values can
    # ever be used.
    processed = []
    for c, vals in by_c.items():
        limit = X // c
        if len(vals) > limit:
            vals.sort(reverse=True)
            vals = vals[:limit]
        for a in vals:
            processed.append((c, a))

    # If all items in this vitamin group have the same calorie cost, the DP
    # is just prefix sums of the best values.
    if len(by_c) == 1:
        c = next(iter(by_c))
        vals = [a for _, a in processed]
        vals.sort(reverse=True)
        limit = min(len(vals), X // c)

        pref = [0] * (limit + 1)
        s = 0
        for i in range(limit):
            s += vals[i]
            pref[i + 1] = s

        dp = [0] * (X + 1)
        for cap in range(X + 1):
            k = cap // c
            if k > limit:
                k = limit
            dp[cap] = pref[k]
        return dp

    # Standard 0/1 knapsack: dp[cap] = maximum vitamin amount with <= cap calories.
    dp = [0] * (X + 1)
    d = dp
    for c, a in processed:
        for cap in range(X, c - 1, -1):
            nv = d[cap - c] + a
            if nv > d[cap]:
                d[cap] = nv

    return dp


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, X = data[0], data[1]
    groups = [[] for _ in range(3)]

    idx = 2
    for _ in range(N):
        v = data[idx]
        a = data[idx + 1]
        c = data[idx + 2]
        idx += 3
        groups[v - 1].append((c, a))

    dps = [build_dp(groups[i], X) for i in range(3)]

    # Make each DP array nondecreasing, so bisect_left can find the minimum
    # calorie capacity needed to reach a target vitamin amount.
    for dp in dps:
        best = dp[0]
        for i in range(1, X + 1):
            if dp[i] < best:
                dp[i] = best
            else:
                best = dp[i]

    lasts = [dp[-1] for dp in dps]
    hi = min(lasts) + 1
    lo = 0
    bl = bisect_left

    def feasible(k):
        total = 0
        for i in range(3):
            if lasts[i] < k:
                return False
            total += bl(dps[i], k)
            if total > X:
                return False
        return True

    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    print(lo)


if __name__ == "__main__":
    solve()