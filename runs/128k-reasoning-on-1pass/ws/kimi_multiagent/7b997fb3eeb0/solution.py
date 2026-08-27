import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    A = [int(x) for x in data[pos:pos + N]]; pos += N
    Q = int(data[pos]); pos += 1

    # need[i] = first index j with A[j] >= 2*A[i] (N if none); p[i] = need[i] - i
    p = [0] * N
    for i in range(N):
        p[i] = bisect_left(A, 2 * A[i]) - i

    # Sparse table for range maximum of p
    log = [0] * (N + 1)
    for i in range(2, N + 1):
        log[i] = log[i >> 1] + 1
    st = [p]
    k = 1
    while (1 << k) <= N:
        prev = st[-1]
        half = 1 << (k - 1)
        st.append(list(map(max, prev[:-half], prev[half:])))
        k += 1

    out = []
    for _ in range(Q):
        l = int(data[pos]) - 1
        r = int(data[pos + 1]) - 1
        pos += 2
        length = r - l + 1
        lo, hi = 0, length >> 1
        while lo < hi:
            mid = (lo + hi + 1) >> 1
            # range max of p over [l, l+mid-1]
            rr = l + mid - 1
            kk = log[mid]
            row = st[kk]
            m = row[l]
            v = row[rr - (1 << kk) + 1]
            if v > m:
                m = v
            if m + mid <= length:
                lo = mid
            else:
                hi = mid - 1
        out.append(str(lo))

    sys.stdout.write("\n".join(out) + "\n")

main()