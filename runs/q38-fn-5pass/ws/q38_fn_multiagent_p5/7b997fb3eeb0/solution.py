import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    A = data[1:1 + N]
    Q = data[1 + N]
    queries = data[2 + N:]
    del data

    sentinel = N + 1
    h = [0] * N
    j = 0

    # h[i] = first index f such that A[f] >= 2*A[i], minus i.
    # If no such index exists, use a sentinel that can never satisfy a query.
    for i in range(N):
        if j < i:
            j = i
        target = A[i] << 1
        while j < N and A[j] < target:
            j += 1
        if j < N:
            h[i] = j - i
        else:
            h[i] = sentinel

    del A

    # Sparse table for range maximum queries on h.
    # Only powers up to floor(N/2) are needed because K <= length/2.
    max_bit = (N >> 1).bit_length() - 1
    st = [h]

    for b in range(1, max_bit + 1):
        half = 1 << (b - 1)
        prev = st[-1]
        length = N - (half << 1) + 1
        curr = [0] * length
        for i in range(length):
            x = prev[i]
            y = prev[i + half]
            curr[i] = x if x >= y else y
        st.append(curr)

    # For binary lifting over K: (block_size, sparse_table_row_for_that_size)
    bits = [(1 << b, st[b]) for b in range(max_bit, -1, -1)]

    out = []
    append = out.append
    to_str = str

    idx = 0
    queries_local = queries
    bits_local = bits

    for _ in range(Q):
        L = queries_local[idx] - 1
        R = queries_local[idx + 1] - 1
        idx += 2

        m = R - L + 1
        M = m >> 1

        K = 0
        cur_max = 0
        rem = M
        limit = m

        # Binary lift the maximum feasible K.
        # cur_max is max h[L .. L+K-1].
        # limit = m - K, rem = M - K.
        for p, row in bits_local:
            if p <= rem:
                new_limit = limit - p
                if cur_max <= new_limit:
                    v = row[L + K]
                    if v <= new_limit:
                        K += p
                        rem -= p
                        limit = new_limit
                        if v > cur_max:
                            cur_max = v

        append(to_str(K))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()