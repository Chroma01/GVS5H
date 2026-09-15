import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    A = data[1:1 + n]
    q = data[1 + n]
    queries = data[2 + n:]
    del data

    # D[i] = p[i] - i, where p[i] is the first index with A[p[i]] >= 2*A[i].
    # If no such index exists, p[i] = n.
    D = [0] * n
    j = 0
    for i in range(n):
        if j <= i:
            j = i + 1
        target = A[i] << 1
        while j < n and A[j] < target:
            j += 1
        D[i] = j - i
    del A

    # floor(log2) table for sparse table queries
    log = [0] * (n + 1)
    for i in range(2, n + 1):
        log[i] = log[i >> 1] + 1

    # Sparse table for range maximum over D.
    # Level k stores max over intervals of length 2^k.
    st = [D]
    step = 1
    while (step << 1) <= n:
        prev = st[-1]
        half = step
        m = n - (half << 1) + 1
        curr = [0] * m
        for i in range(m):
            a = prev[i]
            b = prev[i + half]
            curr[i] = a if a >= b else b
        st.append(curr)
        step <<= 1

    pow2 = [1 << i for i in range(len(st))]

    out = []
    append = out.append
    to_str = str

    st_local = st
    log_local = log
    pow2_local = pow2
    queries_local = queries

    for qi in range(0, 2 * q, 2):
        l = queries_local[qi] - 1
        r = queries_local[qi + 1] - 1
        length = r - l + 1

        hi = length >> 1
        lo = 0

        # Binary search the largest feasible K.
        # K is feasible iff max(D[l .. l+K-1]) <= length - K.
        while lo < hi:
            mid = (lo + hi + 1) >> 1

            k = log_local[mid]
            row = st_local[k]
            off = pow2_local[k]

            mx = row[l]
            v = row[l + mid - off]
            if v > mx:
                mx = v

            if mx <= length - mid:
                lo = mid
            else:
                hi = mid - 1

        append(to_str(lo))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()