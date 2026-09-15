import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N = data[0]
    A = data[1:1 + N]
    Q = data[1 + N]

    # D[p] = q - p, where q is the smallest index with A[q] >= 2 * A[p]
    # If no such index, D[p] = N - p.
    D = [0] * N
    q = 0
    for p in range(N):
        target = 2 * A[p]
        while q < N and A[q] < target:
            q += 1
        if q < N:
            D[p] = q - p
        else:
            D[p] = N - p

    # Sparse table for range maximum over D
    LOG = N.bit_length()
    st = [D]
    j = 1
    while (1 << j) <= N:
        half = 1 << (j - 1)
        prev = st[-1]
        length = N - (1 << j) + 1
        cur = [0] * length
        for i in range(length):
            x = prev[i]
            y = prev[i + half]
            cur[i] = x if x >= y else y
        st.append(cur)
        j += 1

    # Precompute logarithms and powers of two
    log = [0] * (N + 1)
    for i in range(2, N + 1):
        log[i] = log[i >> 1] + 1
    pow2 = [1 << i for i in range(LOG)]

    out = []
    ptr = 2 + N
    for _ in range(Q):
        L = data[ptr]
        R = data[ptr + 1]
        ptr += 2

        l = L - 1
        S = R - L + 1
        lo = 0
        hi = S >> 1

        while lo < hi:
            mid = (lo + hi + 1) >> 1
            end = l + mid - 1
            j = log[mid]
            row = st[j]
            size2 = pow2[j]
            v1 = row[l]
            v2 = row[end - size2 + 1]
            mx = v1 if v1 >= v2 else v2
            if mx + mid <= S:
                lo = mid
            else:
                hi = mid - 1

        out.append(str(lo))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()