import sys


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    K = int(data[0])
    S = data[1]
    T = data[2]
    n = len(S)
    m = len(T)

    if abs(n - m) > K:
        sys.stdout.write("No\n")
        return

    INF = K + 1
    W = 2 * K + 3  # band width: columns j with i-K-1 <= j <= i+K+1

    # Row i uses base b_i = i - K - 1, so column j maps to index j - b_i.
    # curr index for column j: j - i + K + 1
    # prev index for column j: j - i + K + 2  (since b_{i-1} = b_i - 1)
    prev = [INF] * W
    # Row 0: dp[0][j] = j for 0 <= j <= min(m, K); index = j + K + 1
    lim = m if m < K else K
    for j in range(0, lim + 1):
        prev[j + K + 1] = j

    for i in range(1, n + 1):
        curr = [INF] * W
        lo = i - K
        if lo < 0:
            lo = 0
        hi = i + K
        if hi > m:
            hi = m
        si = S[i - 1]
        base_c = K + 1 - i
        base_p = K + 2 - i

        if lo == 0:
            curr[base_c] = i  # dp[i][0] = i (exact)
            best = i
            start = 1
        else:
            # left edge: only deletion from prev[lo] is valid;
            # prev[lo-1] is out of band (INF), curr[lo-1] is INF.
            v = prev[base_p + lo] + 1
            if v > INF:
                v = INF
            curr[base_c + lo] = v
            best = v
            start = lo + 1

        T_local = T
        prev_l = prev
        curr_l = curr
        bc = base_c
        bp = base_p
        for j in range(start, hi + 1):
            # deletion: prev[j] + 1
            v = prev_l[bp + j] + 1
            # insertion: curr[j-1] + 1
            w = curr_l[bc + j - 1] + 1
            if w < v:
                v = w
            # substitution/match: prev[j-1] + cost
            w = prev_l[bp + j - 1] + (0 if si == T_local[j - 1] else 1)
            if w < v:
                v = w
            if v > INF:
                v = INF
            curr_l[bc + j] = v
            if v < best:
                best = v

        if best > K:
            sys.stdout.write("No\n")
            return
        prev = curr

    # answer dp[n][m]; row n base b_n = n - K - 1, index = m - n + K + 1
    ans = prev[m - n + K + 1]
    sys.stdout.write("Yes\n" if ans <= K else "No\n")


if __name__ == "__main__":
    solve()