import sys


def main():
    input = sys.stdin.readline
    n, x = map(int, input().split())

    dp = [[-1] * (x + 1) for _ in range(3)]
    for v in range(3):
        dp[v][0] = 0

    totals = [0, 0, 0]

    for _ in range(n):
        v, a, c = map(int, input().split())
        v -= 1
        totals[v] += a

        cur = dp[v]
        for cal in range(x, c - 1, -1):
            if cur[cal - c] != -1:
                value = cur[cal - c] + a
                if value > cur[cal]:
                    cur[cal] = value

    # Convert exact-calorie DP into at-most-calorie DP.
    for v in range(3):
        cur = dp[v]
        for cal in range(1, x + 1):
            if cur[cal - 1] > cur[cal]:
                cur[cal] = cur[cal - 1]

    upper = min(totals)

    def feasible(target):
        required_total_calories = 0

        for v in range(3):
            cur = dp[v]
            lo, hi = 0, x
            while lo < hi:
                mid = (lo + hi) // 2
                if cur[mid] >= target:
                    hi = mid
                else:
                    lo = mid + 1

            if cur[lo] < target:
                return False

            required_total_calories += lo
            if required_total_calories > x:
                return False

        return True

    lo, hi = 0, upper + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    print(lo)


if __name__ == "__main__":
    main()