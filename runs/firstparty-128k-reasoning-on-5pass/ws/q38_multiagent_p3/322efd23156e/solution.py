import sys
from bisect import bisect_left


def build_dp(items, X):
    items.sort(key=lambda x: (x[0], -x[1]))

    dp = [0] * (X + 1)
    limit = 0
    n = len(items)
    i = 0

    while i < n:
        c = items[i][0]
        if c > X:
            break

        max_count = X // c

        j = i + 1
        while j < n and items[j][0] == c:
            j += 1

        take = j - i
        if take > max_count:
            take = max_count

        for t in range(i, i + take):
            a = items[t][1]
            upper = limit + c
            if upper > X:
                upper = X

            for cap in range(upper, c - 1, -1):
                nv = dp[cap - c] + a
                if nv > dp[cap]:
                    dp[cap] = nv

            limit = upper

        i = j

    for i in range(1, X + 1):
        if dp[i] < dp[i - 1]:
            dp[i] = dp[i - 1]

    return dp


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return

    N, X = data[0], data[1]
    items = [[], [], []]

    idx = 2
    for _ in range(N):
        v = data[idx] - 1
        a = data[idx + 1]
        c = data[idx + 2]
        idx += 3
        if c <= X:
            items[v].append((c, a))

    if not items[0] or not items[1] or not items[2]:
        print(0)
        return

    dps = [
        build_dp(items[0], X),
        build_dp(items[1], X),
        build_dp(items[2], X),
    ]

    lo = 0
    hi = min(dp[-1] for dp in dps) + 1
    bl = bisect_left

    while lo + 1 < hi:
        mid = (lo + hi) // 2
        need = bl(dps[0], mid) + bl(dps[1], mid) + bl(dps[2], mid)
        if need <= X:
            lo = mid
        else:
            hi = mid

    print(lo)


if __name__ == "__main__":
    main()