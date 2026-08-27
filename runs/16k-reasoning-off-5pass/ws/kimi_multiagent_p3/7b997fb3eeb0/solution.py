import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    A = [0] * (N + 1)
    for i in range(1, N + 1):
        A[i] = int(data[pos]); pos += 1

    # h[i] = minimal gap d such that A[i+d] >= 2*A[i]; INF if no such index.
    INF = N + 1
    h = [0] * (N + 1)
    for i in range(1, N + 1):
        j = bisect_left(A, 2 * A[i], i + 1, N + 1)
        h[i] = (j - i) if j <= N else INF

    # Sparse table for range maximum over h[1..N] (1-indexed).
    LOG = [0] * (N + 2)
    for i in range(2, N + 2):
        LOG[i] = LOG[i >> 1] + 1
    st = [h]
    span = 1
    while span * 2 <= N:
        prev = st[-1]
        cur = [0] * (N + 1)
        limit = N - 2 * span + 1
        for i in range(1, limit + 1):
            a = prev[i]
            b = prev[i + span]
            cur[i] = a if a >= b else b
        st.append(cur)
        span *= 2

    def range_max(l, r):
        k = LOG[r - l + 1]
        row = st[k]
        a = row[l]
        b = row[r - (1 << k) + 1]
        return a if a >= b else b

    Q = int(data[pos]); pos += 1
    out = []
    for _ in range(Q):
        L = int(data[pos]); R = int(data[pos + 1]); pos += 2
        m = R - L + 1
        # Smallest gap d in [ceil(m/2), m] with maxH(L, R-d) <= d; answer K = m - d.
        lo = (m + 1) // 2
        hi = m
        while lo < hi:
            mid = (lo + hi) >> 1
            r = R - mid
            if L > r or range_max(L, r) <= mid:
                hi = mid
            else:
                lo = mid + 1
        out.append(str(m - lo))
    sys.stdout.write("\n".join(out) + "\n")

main()