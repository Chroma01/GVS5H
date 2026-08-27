import sys


def main():
    data = sys.stdin.buffer.read().split()
    k = int(data[0])
    s = data[1]
    t = data[2]

    n = len(s)
    m = len(t)

    if abs(n - m) > k:
        print("No")
        return

    inf = k + 1

    # DP row 0: dp[0][j] = j, restricted to the band.
    prev_start = 0
    prev_end = min(m, k)
    prev = list(range(prev_end + 1))

    for i in range(1, n + 1):
        start = max(0, i - k)
        end = min(m, i + k)
        cur = [inf] * (end - start + 1)

        for j in range(start, end + 1):
            best = inf

            # Delete s[i - 1], transitioning from dp[i - 1][j].
            if prev_start <= j <= prev_end:
                value = prev[j - prev_start] + 1
                if value < best:
                    best = value

            # Insert t[j - 1], transitioning from dp[i][j - 1].
            if j > start:
                value = cur[j - 1 - start] + 1
                if value < best:
                    best = value

            # Replace or match, transitioning from dp[i - 1][j - 1].
            if prev_start <= j - 1 <= prev_end:
                value = prev[j - 1 - prev_start] + (s[i - 1] != t[j - 1])
                if value < best:
                    best = value

            cur[j - start] = min(best, inf)

        prev_start, prev_end, prev = start, end, cur

    print("Yes" if prev[ m - prev_start ] <= k else "No")


if __name__ == "__main__":
    main()