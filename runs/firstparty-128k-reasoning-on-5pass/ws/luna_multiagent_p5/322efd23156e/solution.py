import sys
from bisect import bisect_left


def solve():
    input = sys.stdin.buffer.readline
    n, x = map(int, input().split())

    groups = [[], [], []]
    total = [0, 0, 0]

    for _ in range(n):
        v, a, c = map(int, input().split())
        v -= 1
        groups[v].append((a, c))
        total[v] += a

    dps = []

    for group in groups:
        dp = [0] * (x + 1)

        for amount, cost in group:
            for calories in range(x, cost - 1, -1):
                candidate = dp[calories - cost] + amount
                if candidate > dp[calories]:
                    dp[calories] = candidate

        for calories in range(1, x + 1):
            if dp[calories - 1] > dp[calories]:
                dp[calories] = dp[calories - 1]

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
    high = min(total)

    while low < high:
        mid = (low + high + 1) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid - 1

    print(low)


if __name__ == "__main__":
    solve()