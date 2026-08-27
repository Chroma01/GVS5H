import sys
from bisect import bisect_left

def main():
    input = sys.stdin.buffer.readline
    n, x = map(int, input().split())

    dp = [[0] * (x + 1) for _ in range(3)]
    total = [0, 0, 0]

    for _ in range(n):
        v, a, c = map(int, input().split())
        v -= 1
        total[v] += a
        cur = dp[v]
        for cal in range(x, c - 1, -1):
            value = cur[cal - c] + a
            if value > cur[cal]:
                cur[cal] = value

    # Explicitly ensure each DP is an "at most this many calories" profile.
    for v in range(3):
        cur = dp[v]
        best = 0
        for cal in range(x + 1):
            if cur[cal] < best:
                cur[cal] = best
            else:
                best = cur[cal]

    lo = 0
    hi = min(total) + 1

    while hi - lo > 1:
        target = (lo + hi) // 2
        needed = 0

        for v in range(3):
            cost = bisect_left(dp[v], target)
            needed += cost

        if needed <= x:
            lo = target
        else:
            hi = target

    print(lo)

if __name__ == "__main__":
    main()