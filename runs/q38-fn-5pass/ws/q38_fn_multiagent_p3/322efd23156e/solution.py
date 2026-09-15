import sys
from bisect import bisect_left


def compute_dp(items, X):
    # items: list of (calories, vitamin_amount)
    if not items:
        return [0] * (X + 1)

    # dp[c] = maximum vitamin amount with at most c calories,
    # maintained only up to current lim.
    dp = [0] * (X + 1)
    lim = 0

    # Processing smaller calorie items first keeps lim small longer,
    # reducing the total number of DP transitions.
    items.sort()

    d = dp
    rng = range

    for c, a in items:
        new_lim = lim + c
        if new_lim > X:
            new_lim = X

        # Capacities just beyond the old lim inherit the old best value.
        if new_lim > lim:
            fill_val = d[lim]
            if fill_val:
                d[lim + 1:new_lim + 1] = [fill_val] * (new_lim - lim)

        # 0/1 knapsack update, descending to avoid reusing the item.
        for j in rng(new_lim, c - 1, -1):
            v = d[j - c] + a
            if v > d[j]:
                d[j] = v

        lim = new_lim

    # Prefix maximum makes dp[c] valid for all c = 0..X.
    m = 0
    for i in rng(X + 1):
        v = d[i]
        if v < m:
            d[i] = m
        else:
            m = v

    return dp


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, X = data[0], data[1]
    groups = [[], [], []]

    idx = 2
    for _ in range(N):
        v = data[idx]
        a = data[idx + 1]
        c = data[idx + 2]
        idx += 3
        groups[v - 1].append((c, a))

    d0 = compute_dp(groups[0], X)
    d1 = compute_dp(groups[1], X)
    d2 = compute_dp(groups[2], X)

    high = min(d0[X], d1[X], d2[X]) + 1
    low = 0
    bl = bisect_left

    while high - low > 1:
        mid = (low + high) // 2
        need = bl(d0, mid) + bl(d1, mid) + bl(d2, mid)
        if need <= X:
            low = mid
        else:
            high = mid

    print(low)


if __name__ == "__main__":
    solve()