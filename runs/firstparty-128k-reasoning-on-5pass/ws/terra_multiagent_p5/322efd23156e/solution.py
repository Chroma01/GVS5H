import sys
from bisect import bisect_left

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, x = data[0], data[1]
    groups = [[], [], []]
    totals = [0, 0, 0]

    p = 2
    for _ in range(n):
        v = data[p] - 1
        a = data[p + 1]
        c = data[p + 2]
        p += 3
        groups[v].append((a, c))
        totals[v] += a

    dps = []
    for group in groups:
        dp = [0] * (x + 1)

        for a, c in group:
            for cal in range(x, c - 1, -1):
                candidate = dp[cal - c] + a
                if candidate > dp[cal]:
                    dp[cal] = candidate

        for cal in range(1, x + 1):
            if dp[cal - 1] > dp[cal]:
                dp[cal] = dp[cal - 1]

        dps.append(dp)

    upper = min(totals)

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

    low, high = 0, upper + 1
    while high - low > 1:
        mid = (low + high) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid

    print(low)

if __name__ == "__main__":
    main()