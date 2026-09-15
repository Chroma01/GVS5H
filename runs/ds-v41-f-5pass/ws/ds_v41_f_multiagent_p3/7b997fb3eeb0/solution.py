import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    pos = 0
    n = data[pos]; pos += 1
    A = data[pos:pos + n]; pos += n

    # h[j] = nxt[j] - j where nxt[j] = first index k with A[k] >= 2*A[j], else n.
    # A non-decreasing => thresholds 2*A[j] non-decreasing, so two pointers work.
    h = [0] * n
    k = 1
    for i in range(n):
        if k <= i:
            k = i + 1
        t = A[i] << 1
        while k < n and A[k] < t:
            k += 1
        h[i] = k - i

    # Sparse table for range max of h (levels share int objects; only pointers stored).
    st = [h]
    j = 1
    while (1 << j) <= n:
        prev = st[-1]
        half = 1 << (j - 1)
        st.append(list(map(max, prev, prev[half:])))
        j += 1

    # precomputed floor(log2)
    lg = [0] * (n + 1)
    for i in range(2, n + 1):
        lg[i] = lg[i >> 1] + 1

    q = data[pos]; pos += 1
    out = []
    ap = out.append
    for _ in range(q):
        L = data[pos] - 1
        R = data[pos + 1] - 1
        pos += 2
        M = R - L + 1
        lo = (M + 1) >> 1      # D >= ceil(M/2) because K = M - D <= M/2
        hi = M                 # D = M always feasible (empty checked range)
        while lo < hi:
            mid = (lo + hi) >> 1
            r = R - mid        # checked range is [L, R - mid]
            ln = r - L + 1     # here ln >= 1 always (mid <= M-1)
            jj = lg[ln]
            row = st[jj]
            a = row[L]
            b = row[r - (1 << jj) + 1]
            mx = a if a > b else b
            if mx <= mid:
                hi = mid
            else:
                lo = mid + 1
        ap(M - lo)
    sys.stdout.write('\n'.join(map(str, out)))


main()