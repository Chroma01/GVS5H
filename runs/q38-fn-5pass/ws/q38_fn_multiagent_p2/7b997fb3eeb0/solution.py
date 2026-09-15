import sys


def main():
    raw = list(map(int, sys.stdin.buffer.read().split()))
    if not raw:
        return

    N = raw[0]
    A = raw[1:1 + N]
    Q = raw[1 + N]
    queries = raw[2 + N:]
    del raw

    # C[p] = first index j with A[j] >= 2*A[p], minus p.
    # If no such j exists, j = N, which automatically fails all valid queries.
    C = [0] * N
    j = 0
    for p in range(N):
        if j < p + 1:
            j = p + 1
        limit = A[p] << 1
        while j < N and A[j] < limit:
            j += 1
        C[p] = j - p
    del A

    # Sparse table for range maximum queries on C.
    st = [C]
    step = 1
    while (step << 1) <= N:
        prev = st[-1]
        length = N - (step << 1) + 1
        curr = [0] * length
        for i in range(length):
            a = prev[i]
            b = prev[i + step]
            curr[i] = a if a >= b else b
        st.append(curr)
        step <<= 1

    # For each query length, precompute which sparse-table row to use
    # and the offset of the second covering interval.
    off = [0] * (N + 1)
    row_by_len = [None] * (N + 1)
    span = 1
    k = 0
    while span <= N:
        end = span << 1
        if end > N + 1:
            end = N + 1
        row = st[k]
        for length in range(span, end):
            off[length] = length - span
            row_by_len[length] = row
        span = end
        k += 1

    del st, C

    out = []
    append = out.append
    rbl = row_by_len
    offl = off
    qs = queries
    idx = 0

    for _ in range(Q):
        L = qs[idx]
        R = qs[idx + 1]
        idx += 2

        l = L - 1
        D = R - L + 1

        lo = 0
        hi = D >> 1

        while lo < hi:
            mid = (lo + hi + 1) >> 1

            row = rbl[mid]
            a = row[l]
            b = row[l + offl[mid]]
            if b > a:
                a = b

            # Feasible iff max(C[l : l+mid]) + mid <= D.
            if a + mid <= D:
                lo = mid
            else:
                hi = mid - 1

        append(lo)

    del queries, qs, row_by_len, off, rbl, offl

    sys.stdout.write('\n'.join(map(str, out)))


if __name__ == '__main__':
    main()