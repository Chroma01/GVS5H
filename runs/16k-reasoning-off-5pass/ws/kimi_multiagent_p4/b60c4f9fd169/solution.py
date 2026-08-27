import sys

def main():
    data = sys.stdin.buffer.read().split()
    K = int(data[0])
    S = data[1]
    T = data[2]

    if S == T:
        sys.stdout.write("Yes\n")
        return

    n = len(S)
    m = len(T)

    if abs(n - m) > K:
        sys.stdout.write("No\n")
        return

    # Trim common prefix
    lo = 0
    lim = n if n < m else m
    while lo < lim and S[lo] == T[lo]:
        lo += 1

    # Trim common suffix (without overlapping the prefix)
    n2 = n
    m2 = m
    while n2 > lo and m2 > lo and S[n2 - 1] == T[m2 - 1]:
        n2 -= 1
        m2 -= 1

    S = S[lo:n2]
    T = T[lo:m2]
    n = len(S)
    m = len(T)

    if n == 0 or m == 0:
        # One is empty: need |n - m| insertions/deletions
        sys.stdout.write("Yes\n" if abs(n - m) <= K else "No\n")
        return

    if abs(n - m) > K:
        sys.stdout.write("No\n")
        return

    INF = K + 1
    W = 2 * K + 1  # band width, offset = j - i + K

    # Row i=0: dp[j] = j for j in 0..min(m, K)
    prev = [INF] * (W + 1)
    jmax0 = m if m < K else K
    for j in range(0, jmax0 + 1):
        prev[j + K] = j  # i=0, index = j - 0 + K

    for i in range(1, n + 1):
        si = S[i - 1]
        cur = [INF] * (W + 1)
        jlo = i - K
        if jlo < 1:
            jlo = 1
        jhi = i + K
        if jhi > m:
            jhi = m
        row_min = INF
        # handle j = 0 case when i <= K (cost of i deletions)
        if i <= K:
            cur[K - i] = i  # index = 0 - i + K
            row_min = i
        base = K - i  # index = j + base
        for j in range(jlo, jhi + 1):
            idx = j + base
            # deletion: from prev row, same j -> prev[idx]
            best = prev[idx] + 1
            # insertion: from cur row, j-1 -> cur[idx-1]
            v = cur[idx - 1] + 1
            if v < best:
                best = v
            # match/substitution: from prev row, j-1 -> prev[idx-1]
            v = prev[idx - 1] + (0 if si == T[j - 1] else 1)
            if v < best:
                best = v
            cur[idx] = best
            if best < row_min:
                row_min = best
        if row_min > K:
            sys.stdout.write("No\n")
            return
        prev = cur

    # answer cell: i=n, j=m, index = m - n + K
    sys.stdout.write("Yes\n" if prev[m - n + K] <= K else "No\n")

main()