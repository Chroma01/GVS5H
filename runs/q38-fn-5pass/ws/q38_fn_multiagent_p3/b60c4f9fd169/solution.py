import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    K = int(data[0])
    S = data[1]
    T = data[2]

    n0 = len(S)
    m0 = len(T)

    if abs(n0 - m0) > K:
        sys.stdout.write("No\n")
        return

    # Trim common prefix.
    p = 0
    lim = n0 if n0 < m0 else m0
    while p < lim and S[p] == T[p]:
        p += 1

    if p == n0 or p == m0:
        sys.stdout.write("Yes\n")
        return

    # Trim common suffix.
    q = 0
    rem = lim - p
    while q < rem and S[n0 - 1 - q] == T[m0 - 1 - q]:
        q += 1

    if p or q:
        S = S[p:n0 - q]
        T = T[p:m0 - q]

    n = len(S)
    m = len(T)

    if n == 0 or m == 0:
        sys.stdout.write("Yes\n" if max(n, m) <= K else "No\n")
        return

    if abs(n - m) > K:
        sys.stdout.write("No\n")
        return

    # Iterate over the shorter string as rows.
    if n > m:
        S, T = T, S
        n, m = m, n

    # Always possible by substituting min(n,m) characters and inserting/deleting the rest.
    if max(n, m) <= K:
        sys.stdout.write("Yes\n")
        return

    if K == 0:
        sys.stdout.write("Yes\n" if S == T else "No\n")
        return

    # Final diagonal offset after making n <= m.
    d = m - n

    # Any path of cost <= K must satisfy |offset| + |d - offset| <= K.
    extra = (K - d) // 2
    base_lo = -extra
    base_hi = d + extra

    INF = 10**9
    SHIFT = K + 1
    W = 2 * K + 3

    prev = [INF] * W
    cur = [INF] * W

    # Row 0: dp[0][j] = j, only for offsets inside the narrowed band.
    hi0 = base_hi if base_hi < m else m
    for o in range(hi0 + 1):
        prev[SHIFT + o] = o

    # Sentinel at index 0 lets us use j directly as an index into T2.
    T2 = b" " + T

    inf = INF
    sh = SHIFT
    bl = base_lo
    bh = base_hi
    mm = m
    kk = K
    tt = T2

    for i, sc in enumerate(S, 1):
        lo = bl
        ni = -i
        if ni > lo:
            lo = ni

        hi = bh
        tmp = mm - i
        if tmp < hi:
            hi = tmp

        if lo > hi:
            sys.stdout.write("No\n")
            return

        start = lo + sh
        end = hi + sh + 1

        # Immediate outside the current valid interval must be INF.
        cur[start - 1] = inf
        cur[end] = inf

        p = prev
        c = cur
        t_idx = i + lo
        row_min = inf

        for idx in range(start, end):
            # substitution / match from diagonal
            v = p[idx] + (sc != tt[t_idx])

            # deletion from previous row, same j: previous offset is o + 1
            u = p[idx + 1] + 1
            if u < v:
                v = u

            # insertion from current row, previous j: current offset is o - 1
            l = c[idx - 1] + 1
            if l < v:
                v = l

            c[idx] = v
            if v < row_min:
                row_min = v

            t_idx += 1

        if row_min > kk:
            sys.stdout.write("No\n")
            return

        prev, cur = cur, prev

    final_idx = (m - n) + sh
    sys.stdout.write("Yes\n" if prev[final_idx] <= kk else "No\n")


if __name__ == "__main__":
    solve()