import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    K = int(data[0])
    S = data[1]
    T = data[2]

    write = sys.stdout.write
    YES = "Yes\n"
    NO = "No\n"

    if S == T:
        write(YES)
        return

    n = len(S)
    m = len(T)

    if abs(n - m) > K:
        write(NO)
        return

    if K == 0:
        write(NO)
        return

    # Edit distance is symmetric. Keep the shorter string as S.
    if n > m:
        S, T = T, S
        n, m = m, n

    # If the longer string has length at most K, we can replace the shorter
    # string and insert the remaining characters in at most m operations.
    if K >= m:
        write(YES)
        return

    # Trim common prefix and suffix. This is safe and often reduces work.
    p = 0
    while p < n and S[p] == T[p]:
        p += 1

    q = 0
    limit = n - p
    n1 = n - 1
    m1 = m - 1
    while q < limit and S[n1 - q] == T[m1 - q]:
        q += 1

    if p or q:
        S = S[p:n - q]
        T = T[p:m - q]
        n -= p + q
        m -= p + q

    if n == 0:
        write(YES if m <= K else NO)
        return

    if K >= m:
        write(YES)
        return

    # Banded Ukkonen DP.
    INF = K + 1
    width = 2 * K + 2

    prev = [INF] * width
    for j in range(K + 1):
        prev[j + K] = j
    curr = [INF] * width

    # Sentinel makes T[0] safe for the j = 0 column.
    T = b'\0' + T

    twoK = 2 * K
    m_minus_K = m - K
    m_plus_K = m + K

    for i, si in enumerate(S, 1):
        if i <= K:
            idx_low = K - i
            j = 0
        else:
            idx_low = 0
            j = i - K

        if i <= m_minus_K:
            idx_high = twoK
        else:
            idx_high = m_plus_K - i
        idx_high_plus = idx_high + 1

        left = INF
        row_min = INF

        for idx in range(idx_low, idx_high_plus):
            # Delete from S: dp[i-1][j] + 1
            v = prev[idx + 1] + 1

            # Insert into S: dp[i][j-1] + 1
            lv = left + 1
            if lv < v:
                v = lv

            # Match or substitute: dp[i-1][j-1] + cost
            d = prev[idx] + (si != T[j])
            if d < v:
                v = d

            if v > K:
                v = INF

            curr[idx] = v
            if v < row_min:
                row_min = v

            left = v
            j += 1

        if row_min > K:
            write(NO)
            return

        # Keep immediate outside-band sentinels clean for the next row.
        if idx_low:
            curr[idx_low - 1] = INF
        curr[idx_high_plus] = INF

        prev, curr = curr, prev

    ans = prev[m - n + K]
    write(YES if ans <= K else NO)


if __name__ == "__main__":
    solve()