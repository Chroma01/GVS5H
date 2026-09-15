import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    p = 0
    N = data[p]
    p += 1

    A = data[p:p + N]
    p += N

    Q = data[p]
    p += 1

    n = N

    # D[i] = nxt[i] - i, where nxt[i] is the first index j with A[j] >= 2*A[i].
    # If no such j exists, nxt[i] = n, which is a safe sentinel.
    D = [0] * n
    j = 0
    for i in range(n):
        if j < i:
            j = i
        target = A[i] << 1
        while j < n and A[j] < target:
            j += 1
        D[i] = j - i

    del A

    # Sparse table for range maximum queries on D.
    # Level b stores maximums over blocks of length 2^b.
    st = [D]
    st_append = st.append
    step = 1
    while (step << 1) <= n:
        half = step
        step <<= 1
        limit = n - step + 1
        prev = st[-1]
        st_append([
            prev[i] if prev[i] >= prev[i + half] else prev[i + half]
            for i in range(limit)
        ])

    out = []
    append = out.append
    st_local = st
    D_local = D

    for _ in range(Q):
        L = data[p] - 1
        R = data[p + 1] - 1
        p += 2

        m = R - L + 1

        # K is feasible iff max(D[L .. L+K-1]) <= m-K.
        # Also K <= m//2 and K <= m-D[L].
        hi = m >> 1
        cap = m - D_local[L]
        if cap < hi:
            hi = cap

        if hi <= 0:
            append("0")
            continue

        # Binary lifting on the monotone feasibility predicate.
        length = 0
        curmax = 0
        b = hi.bit_length() - 1
        step = 1 << b

        while step:
            end = length + step
            if end <= hi:
                mx = st_local[b][L + length]
                bound = m - end

                if mx > curmax:
                    if mx <= bound:
                        length = end
                        curmax = mx
                else:
                    if curmax <= bound:
                        length = end

            step >>= 1
            b -= 1

        append(str(length))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()