import sys

def main():
    input = sys.stdin.buffer.readline

    K = int(input())
    s = input().strip()
    t = input().strip()

    if abs(len(s) - len(t)) > K:
        print("No")
        return

    # Remove equal prefix.
    p = 0
    limit = min(len(s), len(t))
    while p < limit and s[p] == t[p]:
        p += 1
    s = s[p:]
    t = t[p:]

    # Remove equal suffix from the remaining parts.
    q = 0
    limit = min(len(s), len(t))
    while q < limit and s[len(s) - 1 - q] == t[len(t) - 1 - q]:
        q += 1
    if q:
        s = s[:-q]
        t = t[:-q]

    if abs(len(s) - len(t)) > K:
        print("No")
        return

    # Use the shorter string as the source-prefix dimension.
    if len(s) > len(t):
        s, t = t, s

    n = len(s)
    m = len(t)
    INF = K + 1

    # Row i=0: only insertions are possible.
    prev_lo = 0
    prev_hi = min(m, K)
    prev = list(range(prev_hi + 1))

    for i in range(1, n + 1):
        lo = max(0, i - K)
        hi = min(m, i + K)
        cur = [INF] * (hi - lo + 1)

        si = s[i - 1]
        prev_len = len(prev)

        for idx, j in enumerate(range(lo, hi + 1)):
            best = INF

            # Delete s[i-1]: dp[i-1][j] + 1
            pidx = j - prev_lo
            if 0 <= pidx < prev_len:
                value = prev[pidx] + 1
                if value < best:
                    best = value

            # Replace/match: dp[i-1][j-1] + (s[i-1] != t[j-1])
            if j > 0:
                pidx -= 1
                if 0 <= pidx < prev_len:
                    value = prev[pidx] + (si != t[j - 1])
                    if value < best:
                        best = value

            # Insert t[j-1]: dp[i][j-1] + 1
            if idx > 0:
                value = cur[idx - 1] + 1
                if value < best:
                    best = value

            if best <= K:
                cur[idx] = best

        prev = cur
        prev_lo = lo
        prev_hi = hi

    if prev_lo <= m <= prev_hi and prev[m - prev_lo] <= K:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()