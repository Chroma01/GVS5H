import sys
from bisect import bisect_left


def build_dp(items, limit):
    dp = [0] * (limit + 1)

    for amount, cost in items:
        for capacity in range(limit, cost - 1, -1):
            candidate = dp[capacity - cost] + amount
            if candidate > dp[capacity]:
                dp[capacity] = candidate

    for capacity in range(1, limit + 1):
        if dp[capacity] < dp[capacity - 1]:
            dp[capacity] = dp[capacity - 1]

    return dp


def solve():
    input = sys.stdin.buffer.readline
    n, x = map(int, input().split())

    groups = [[], [], []]
    sums = [0, 0, 0]

    for _ in range(n):
        vitamin, amount, calories = map(int, input().split())
        groups[vitamin - 1].append((amount, calories))
        sums[vitamin - 1] += amount

    dps = [build_dp(group, x) for group in groups]

    def feasible(target):
        required_calories = 0
        for dp in dps:
            capacity = bisect_left(dp, target)
            if capacity > x:
                return False
            required_calories += capacity
        return required_calories <= x

    low, high = 0, min(sums)

    while low < high:
        mid = (low + high + 1) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid - 1

    print(low)


if __name__ == "__main__":
    solve()