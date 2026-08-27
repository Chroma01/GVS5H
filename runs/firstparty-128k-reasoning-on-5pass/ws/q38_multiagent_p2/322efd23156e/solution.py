import sys
from bisect import bisect_left


def prune(items, X):
    # For a fixed vitamin and calorie cost c, at most X // c foods of that
    # cost can ever be used. Keep only the largest such amounts.
    if not items:
        return items

    items.sort()  # sorted by (cost, amount)
    res = []
    n = len(items)
    i = 0
    while i < n:
        c = items[i][0]
        limit = X // c
        j = i + 1
        while j < n and items[j][0] == c:
            j += 1

        if j - i > limit:
            res.extend(items[j - limit:j])
        else:
            res.extend(items[i:j])
        i = j

    return res


def build_dp(items, X):
    # dp[c] = maximum vitamin amount obtainable with at most c calories.
    dp = [0] * (X + 1)
    cur = 0  # max total cost reachable from processed items, capped by X

    for c, a in items:
        new_cur = cur + c
        if new_cur > X:
            new_cur = X

        # Make capacities newly reachable by this item represent "not taking it".
        if new_cur > cur:
            best = dp[cur]
            if new_cur == cur + 1:
                dp[cur + 1] = best
            else:
                dp[cur + 1:new_cur + 1] = [best] * (new_cur - cur)

        # 0/1 knapsack update, descending to avoid reusing the item.
        for cap in range(new_cur, c - 1, -1):
            nv = dp[cap - c] + a
            if nv > dp[cap]:
                dp[cap] = nv

        cur = new_cur

    # Ensure at-most capacity semantics over the whole range.
    for i in range(1, X + 1):
        if dp[i] < dp[i - 1]:
            dp[i] = dp[i - 1]

    return dp


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, X = data[0], data[1]
    items = [[] for _ in range(3)]
    p = 2

    for _ in range(N):
        v = data[p] - 1
        a = data[p + 1]
        c = data[p + 2]
        p += 3
        if c <= X:
            items[v].append((c, a))

    # If any vitamin is unavailable, the minimum is always 0.
    if not items[0] or not items[1] or not items[2]:
        print(0)
        return

    dps = [build_dp(prune(items[v], X), X) for v in range(3)]

    lo = 0
    hi = min(dp[X] for dp in dps)
    bl = bisect_left

    while lo < hi:
        mid = (lo + hi + 1) // 2
        total = 0
        ok = True

        for dp in dps:
            pos = bl(dp, mid)
            if pos > X:
                ok = False
                break
            total += pos
            if total > X:
                ok = False
                break

        if ok:
            lo = mid
        else:
            hi = mid - 1

    print(lo)


if __name__ == "__main__":
    main()