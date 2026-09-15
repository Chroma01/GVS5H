import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    write = sys.stdout.write
    K = int(data[0])
    S = data[1]
    T = data[2]

    n = len(S)
    m = len(T)

    if S == T:
        write("Yes\n")
        return

    # Any two strings can be transformed in at most max(len(S), len(T)) edits.
    if K >= max(n, m):
        write("Yes\n")
        return

    if abs(n - m) > K:
        write("No\n")
        return

    # Use the shorter string as the row dimension.
    if n > m:
        S, T = T, S
        n, m = m, n

    delta = m - n

    # Tight diagonal bounds.
    # If a successful path uses I insertions and D deletions:
    #   I - D = delta, I + D <= K
    # so I <= floor((K + delta) / 2), D <= floor((K - delta) / 2).
    # Therefore every intermediate diagonal d = j - i lies in:
    #   -D <= d <= I
    Dlo = -((K - delta) // 2)
    Dhi = (K + delta) // 2

    # Physical bounds: 0 <= i <= n, 0 <= j <= m, so -n <= d <= m.
    if Dlo < -n:
        Dlo = -n
    if Dhi > m:
        Dhi = m

    W = Dhi - Dlo + 1
    INF = K + 1

    # Index 0 and W+1 are padding INF.
    size = W + 2
    prev = [INF] * size
    curr = [INF] * size
    inf_list = [INF] * W
    W1 = W + 1

    # Row 0: dp[0][j] = j, where d = j.
    start = Dlo
    if start < 0:
        start = 0
    end = Dhi
    if end > m:
        end = m

    for d in range(start, end + 1):
        val = d
        if val > INF:
            val = INF
        prev[d - Dlo + 1] = val

    if n == 0:
        idx = delta - Dlo + 1
        write("Yes\n" if prev[idx] <= K else "No\n")
        return

    # Rows where the whole diagonal band is inside [0, m].
    # In these rows every curr[1..W] is overwritten, so no clearing is needed.
    full_start = -Dlo
    if full_start < 1:
        full_start = 1
    full_end = m - Dhi
    if full_end > n:
        full_end = n

    # Local bindings for speed.
    S_local = S
    T_local = T
    K_local = K
    INF_local = INF
    Dlo_local = Dlo
    Dhi_local = Dhi
    m_local = m
    W1_local = W1
    inf_list_local = inf_list
    full_start_local = full_start
    full_end_local = full_end
    idx_list = list(range(1, W1_local))

    for i in range(1, n + 1):
        if full_start_local <= i <= full_end_local:
            # Full band: d = Dlo, Dlo+1, ..., Dhi.
            t_idx = i + Dlo_local - 1
            idx_iter = idx_list
        else:
            # Boundary row: clear, then fill only the clipped valid diagonals.
            curr[1:W1_local] = inf_list_local

            lo = -i
            if lo < Dlo_local:
                lo = Dlo_local
            hi = m_local - i
            if hi > Dhi_local:
                hi = Dhi_local

            if lo > hi:
                write("No\n")
                return

            lo_idx = lo - Dlo_local + 1
            hi_idx = hi - Dlo_local + 1
            t_idx = i + lo - 1
            idx_iter = range(lo_idx, hi_idx + 1)

        si = S_local[i - 1]
        row_min = INF_local

        for idx in idx_iter:
            # Substitute / match from prev same diagonal.
            v = prev[idx] + (si != T_local[t_idx])

            # Delete from S: previous diagonal d + 1.
            a = prev[idx + 1] + 1
            if a < v:
                v = a

            # Insert into S: current diagonal d - 1.
            b = curr[idx - 1] + 1
            if b < v:
                v = b

            # Values above K are useless; cap them to keep integers small.
            if v > INF_local:
                v = INF_local

            curr[idx] = v
            if v < row_min:
                row_min = v

            t_idx += 1

        if row_min > K_local:
            write("No\n")
            return

        prev, curr = curr, prev

    final_idx = delta - Dlo + 1
    write("Yes\n" if prev[final_idx] <= K else "No\n")


if __name__ == "__main__":
    main()