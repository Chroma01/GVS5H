import sys

def solve():
    data = sys.stdin.buffer.read().split()
    K = int(data[0])
    S = data[1]
    T = data[2]
    n = len(S)
    m = len(T)

    if abs(n - m) > K:
        sys.stdout.write("No\n")
        return

    INF = 10**9
    # dp[j] = edit distance between S[:i] and T[:j] for current row i.
    # Row 0: distance from empty prefix of S to T[:j] is j (all inserts).
    dp = list(range(m + 1))

    for i in range(1, n + 1):
        lo = i - K
        if lo < 1:
            lo = 1
        hi = i + K
        if hi > m:
            hi = m

        new = [INF] * (m + 1)
        # Column 0: deleting all i characters of S[:i].
        if i <= K:
            new[0] = i

        si = S[i - 1]
        prev = dp
        best = INF
        # Cells just outside the band are treated as INF (unreachable within K edits).
        left = prev[lo - 1] if lo > 1 else prev[0]
        for j in range(lo, hi + 1):
            cur = prev[j]          # dp[i-1][j]   (deletion)
            diag = left            # dp[i-1][j-1] (substitution / match)
            left = cur
            if si == T[j - 1]:
                v = diag
            else:
                v = diag + 1
            if cur + 1 < v:
                v = cur + 1
            below = new[j - 1] + 1  # dp[i][j-1]   (insertion)
            if below < v:
                v = below
            new[j] = v
            if v < best:
                best = v

        if best > K:
            sys.stdout.write("No\n")
            return
        dp = new

    sys.stdout.write("Yes\n" if dp[m] <= K else "No\n")

if __name__ == "__main__":
    solve()