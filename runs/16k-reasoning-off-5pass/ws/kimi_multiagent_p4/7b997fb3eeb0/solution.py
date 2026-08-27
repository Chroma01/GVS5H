import sys
from bisect import bisect_left

def solve():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    A = list(map(int, data[pos:pos + N])); pos += N
    Q = int(data[pos]); pos += 1

    # g[j] = smallest index with A[g[j]] >= 2*A[j], or N if none (infinity)
    # H[j] = g[j] - j
    H = [0] * N
    for j in range(N):
        g = bisect_left(A, 2 * A[j])
        H[j] = g - j  # if g == N, H[j] = N - j acts as infinity

    # Sparse table for range max
    st = [H]
    k = 1
    while (1 << k) <= N:
        prev = st[-1]
        length = N - (1 << k) + 1
        half = 1 << (k - 1)
        cur = [0] * length
        for i in range(length):
            a = prev[i]
            b = prev[i + half]
            cur[i] = a if a >= b else b
        st.append(cur)
        k += 1

    log2 = [0] * (N + 2)
    for i in range(2, N + 1):
        log2[i] = log2[i >> 1] + 1

    def range_max(l, r):  # inclusive
        length = r - l + 1
        kk = log2[length]
        a = st[kk][l]
        b = st[kk][r - (1 << kk) + 1]
        return a if a >= b else b

    out = []
    for _ in range(Q):
        L = int(data[pos]); R = int(data[pos + 1]); pos += 2
        L -= 1; R -= 1
        length = R - L + 1
        lo, hi = 0, length // 2
        # binary search max feasible K
        while lo < hi:
            mid = (lo + hi + 1) // 2
            # check: max H over [L, L+mid-1] <= R - L - mid + 1
            if range_max(L, L + mid - 1) <= R - L - mid + 1:
                lo = mid
            else:
                hi = mid - 1
        out.append(str(lo))

    sys.stdout.write("\n".join(out) + "\n")

solve()