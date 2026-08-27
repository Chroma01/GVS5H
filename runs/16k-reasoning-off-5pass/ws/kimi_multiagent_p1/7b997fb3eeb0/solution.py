import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    A = [int(x) for x in data[pos:pos + N]]; pos += N
    Q = int(data[pos]); pos += 1

    # f[i] = smallest index j (0-indexed) with A[j] >= 2*A[i]; sentinel N if none
    # M[i] = f[i] - i
    M = [0] * N
    for i in range(N):
        j = bisect_left(A, 2 * A[i])
        M[i] = j - i  # if j == N (sentinel), M[i] = N - i, large enough to fail checks

    # Sparse table for range maximum on M
    LOG = [0] * (N + 1)
    for i in range(2, N + 1):
        LOG[i] = LOG[i >> 1] + 1
    st = [M]
    j = 1
    while (1 << j) <= N:
        prev = st[-1]
        length = N - (1 << j) + 1
        half = 1 << (j - 1)
        cur = [0] * length
        for i in range(length):
            a = prev[i]
            b = prev[i + half]
            cur[i] = a if a >= b else b
        st.append(cur)
        j += 1

    def range_max(l, r):  # inclusive, 0-indexed, l <= r
        k = LOG[r - l + 1]
        a = st[k][l]
        b = st[k][r - (1 << k) + 1]
        return a if a >= b else b

    out = []
    for _ in range(Q):
        L = int(data[pos]); R = int(data[pos + 1]); pos += 2
        l = L - 1
        r = R - 1
        length = r - l + 1
        lo, hi = 0, length // 2
        # find max k in [0, hi] such that rangeMax(M, l, l+k-1) <= r - k + 1 - l
        while lo < hi:
            mid = (lo + hi + 1) >> 1
            if range_max(l, l + mid - 1) <= r - mid + 1 - l:
                lo = mid
            else:
                hi = mid - 1
        out.append(str(lo))

    sys.stdout.write("\n".join(out) + "\n")

main()