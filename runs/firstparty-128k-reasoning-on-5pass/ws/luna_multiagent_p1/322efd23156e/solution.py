import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, X = data[0], data[1]
    groups = [[], [], []]
    totals = [0, 0, 0]

    index = 2
    for _ in range(n):
        vitamin, amount, calories = data[index], data[index + 1], data[index + 2]
        index += 3
        vitamin -= 1
        groups[vitamin].append((amount, calories))
        totals[vitamin] += amount

    dps = []
    for items in groups:
        dp = [0] * (X + 1)
        for amount, calories in items:
            for capacity in range(X, calories - 1, -1):
                candidate = dp[capacity - calories] + amount
                if candidate > dp[capacity]:
                    dp[capacity] = candidate
        dps.append(dp)

    def minimum_cost(dp, target):
        if dp[X] < target:
            return X + 1

        left, right = 0, X
        while left < right:
            middle = (left + right) // 2
            if dp[middle] >= target:
                right = middle
            else:
                left = middle + 1
        return left

    def feasible(target):
        required = 0
        for dp in dps:
            required += minimum_cost(dp, target)
            if required > X:
                return False
        return True

    left, right = 0, min(totals)
    while left < right:
        middle = (left + right + 1) // 2
        if feasible(middle):
            left = middle
        else:
            right = middle - 1

    print(left)


if __name__ == "__main__":
    solve()