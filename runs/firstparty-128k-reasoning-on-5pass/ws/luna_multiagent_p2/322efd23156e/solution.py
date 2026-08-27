import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, x = data[0], data[1]
    groups = [[], [], []]
    total_amount = [0, 0, 0]

    p = 2
    for _ in range(n):
        v, a, c = data[p], data[p + 1], data[p + 2]
        p += 3
        idx = v - 1
        groups[idx].append((a, c))
        total_amount[idx] += a

    dps = []
    for items in groups:
        dp = [-1] * (x + 1)
        dp[0] = 0

        for amount, calorie in items:
            for cost in range(x, calorie - 1, -1):
                previous = dp[cost - calorie]
                if previous >= 0:
                    candidate = previous + amount
                    if candidate > dp[cost]:
                        dp[cost] = candidate

        dps.append(dp)

    def minimum_cost(dp, target):
        if target == 0:
            return 0
        for cost, amount in enumerate(dp):
            if amount >= target:
                return cost
        return x + 1

    def feasible(target):
        total_cost = 0
        for dp in dps:
            cost = minimum_cost(dp, target)
            total_cost += cost
            if total_cost > x:
                return False
        return True

    low = 0
    high = min(total_amount) + 1

    while high - low > 1:
        mid = (low + high) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid

    print(low)


if __name__ == "__main__":
    main()