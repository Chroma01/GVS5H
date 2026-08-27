import sys
from bisect import bisect_left


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, x = data[0], data[1]
    foods = [[], [], []]
    totals = [0, 0, 0]

    p = 2
    for _ in range(n):
        v, a, c = data[p], data[p + 1], data[p + 2]
        p += 3
        foods[v - 1].append((a, c))
        totals[v - 1] += a

    dps = []
    for group in foods:
        dp = [0] * (x + 1)

        for a, c in group:
            for calorie in range(x, c - 1, -1):
                value = dp[calorie - c] + a
                if value > dp[calorie]:
                    dp[calorie] = value

        for calorie in range(1, x + 1):
            if dp[calorie] < dp[calorie - 1]:
                dp[calorie] = dp[calorie - 1]

        dps.append(dp)

    low = 0
    high = min(totals) + 1

    while high - low > 1:
        mid = (low + high) // 2

        needed = 0
        for dp in dps:
            needed += bisect_left(dp, mid)

        if needed <= x:
            low = mid
        else:
            high = mid

    print(low)


if __name__ == "__main__":
    main()