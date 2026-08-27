import sys


def solve() -> None:
    input = sys.stdin.buffer.readline

    k = int(input())
    s = input().strip()
    t = input().strip()

    n = len(s)
    m = len(t)

    if abs(n - m) > k:
        print("No")
        return

    inf = k + 1
    width = 2 * k + 3

    # Row 0: dp[0][j] = j for j within the band.
    prev = [inf] * width
    prev_lo = 0
    prev_hi = min(m, k)
    for j in range(prev_hi + 1):
        prev[j] = j

    cur = [inf] * width

    for i in range(1, n + 1):
        lo = max(0, i - k)
        hi = min(m, i + k)

        if lo == 0:
            cur[0] = i

        start = max(1, lo)
        si = s[i - 1]

        for j in range(start, hi + 1):
            best = inf

            # Delete s[i - 1].
            if j <= prev_hi:
                best = prev[j - prev_lo] + 1

            # Insert t[j - 1].
            if j > lo:
                value = cur[j - 1 - lo] + 1
                if value < best:
                    best = value

            # Match or replace.
            if prev_lo <= j - 1 <= prev_hi:
                value = prev[j - 1 - prev_lo] + (si != t[j - 1])
                if value < best:
                    best = value

            cur[j - lo] = best

        prev, cur = cur, prev
        prev_lo, prev_hi = lo, hi

    answer = prev[m - prev_lo] <= k
    print("Yes" if answer else "No")


if __name__ == "__main__":
    solve()