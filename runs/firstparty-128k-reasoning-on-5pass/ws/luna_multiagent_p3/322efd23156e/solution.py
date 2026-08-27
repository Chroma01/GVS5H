import sys
from bisect import bisect_left


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, x = data[0], data[1]

    groups = [[], [], []]
    totals = [0, 0, 0]

    pos = 2
    for _ in range(n):
        v, a, c = data[pos], data[pos + 1], data[pos + 2]
        pos += 3
        groups[v - 1].append((a, c))
        totals[v - 1] += a

    dps = []
    for items in groups:
        dp = [0] * (x + 1)
        for amount, cost in items:
            for calorie in range(x, cost - 1, -1):
                candidate = dp[calorie - cost] + amount
                if candidate > dp[calorie]:
                    dp[calorie] = candidate
        dps.append(dp)

    def feasible(target):
        required = 0
        for dp in dps:
            cost = bisect_left(dp, target)
            if cost > x:
                return False
            required += cost
            if required > x:
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