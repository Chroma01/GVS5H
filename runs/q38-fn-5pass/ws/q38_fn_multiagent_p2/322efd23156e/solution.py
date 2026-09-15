import sys
from bisect import bisect_left


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, x = data[0], data[1]
    groups = [[], [], []]

    idx = 2
    for _ in range(n):
        v = data[idx]
        a = data[idx + 1]
        c = data[idx + 2]
        idx += 3
        groups[v - 1].append((c, a))

    # If some vitamin cannot be obtained at all, the answer is 0.
    if not groups[0] or not groups[1] or not groups[2]:
        print(0)
        return

    # If even the cheapest food from each vitamin group exceeds the budget,
    # achieving at least 1 of every vitamin is impossible.
    min_cost_sum = 0
    for g in groups:
        min_cost_sum += min(c for c, _ in g)
    if min_cost_sum > x:
        print(0)
        return

    dps = []

    for items in groups:
        dp = [0] * (x + 1)

        if items:
            # Processing smaller costs first tends to keep the active DP range small.
            items.sort()

            s = 0
            d = dp

            for c, a in items:
                ns = s + c
                if ns > x:
                    ns = x

                # Capacities just beyond the previous total cost can already take
                # all previously processed items, so their old value is dp[s].
                if ns > s:
                    d[s + 1:ns + 1] = [d[s]] * (ns - s)

                # 0/1 knapsack update, descending to avoid reusing this item.
                for w in range(ns, c - 1, -1):
                    nv = d[w - c] + a
                    if nv > d[w]:
                        d[w] = nv

                s = ns

            # Make dp[c] mean "maximum vitamin amount with at most c calories"
            # and nondecreasing, so bisect_left can find the minimum needed calories.
            best = 0
            for i in range(x + 1):
                if d[i] < best:
                    d[i] = best
                else:
                    best = d[i]

        dps.append(dp)

    high = min(dp[x] for dp in dps)

    lo = 0
    hi = high + 1
    bl = bisect_left

    while hi - lo > 1:
        mid = (lo + hi) // 2
        total = 0

        for dp in dps:
            total += bl(dp, mid)
            if total > x:
                break

        if total <= x:
            lo = mid
        else:
            hi = mid

    print(lo)


if __name__ == "__main__":
    solve()