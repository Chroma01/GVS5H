import sys
from bisect import bisect_left


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, x = data[0], data[1]

    groups = [[], [], []]
    total = [0, 0, 0]

    pos = 2
    for _ in range(n):
        v, a, c = data[pos], data[pos + 1], data[pos + 2]
        pos += 3
        groups[v - 1].append((a, c))
        total[v - 1] += a

    dps = []
    neg_inf = -10**30

    for items in groups:
        dp = [neg_inf] * (x + 1)
        dp[0] = 0

        for amount, cost in items:
            for capacity in range(x, cost - 1, -1):
                previous = dp[capacity - cost]
                if previous != neg_inf:
                    candidate = previous + amount
                    if candidate > dp[capacity]:
                        dp[capacity] = candidate

        best = neg_inf
        for capacity in range(x + 1):
            if dp[capacity] < best:
                dp[capacity] = best
            else:
                best = dp[capacity]

        dps.append(dp)

    def feasible(target):
        required = 0
        for dp in dps:
            capacity = bisect_left(dp, target)
            if capacity > x:
                return False
            required += capacity
            if required > x:
                return False
        return True

    low = 0
    high = min(total) + 1

    while high - low > 1:
        mid = (low + high) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid

    print(low)


if __name__ == "__main__":
    solve()