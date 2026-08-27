import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    A = [0] * (N + 2)  # 1-indexed
    for i in range(1, N + 1):
        A[i] = int(data[pos]); pos += 1
    Q = int(data[pos]); pos += 1
    queries = []
    for _ in range(Q):
        L = int(data[pos]); R = int(data[pos + 1]); pos += 2
        queries.append((L, R))

    # g[i] = smallest index j with A[j] >= 2*A[i], or N+1 if none
    w = [0] * (N + 2)
    for i in range(1, N + 1):
        j = bisect_left(A, 2 * A[i], i + 1, N + 1)
        if j == N + 1:
            w[i] = N + 1  # impossible to use i as a top
        else:
            w[i] = j - i

    # Sparse table for range max over w[1..N]
    LOG = max(1, N.bit_length())
    st = [w[1:N + 1]]  # st[k] has length N - 2^k + 1
    k = 1
    while (1 << k) <= N:
        prev = st[-1]
        half = 1 << (k - 1)
        cur = [0] * (N - (1 << k) + 1)
        for i in range(len(cur)):
            a = prev[i]
            b = prev[i + half]
            cur[i] = a if a >= b else b
        st.append(cur)
        k += 1
    log2 = [0] * (N + 2)
    for i in range(2, N + 1):
        log2[i] = log2[i >> 1] + 1

    def range_max(l, r):
        # max of w[l..r], 1-indexed, l <= r
        length = r - l + 1
        kk = log2[length]
        row = st[kk]
        a = row[l - 1]
        b = row[r - (1 << kk)]
        return a if a >= b else b

    out = []
    for L, R in queries:
        m = R - L + 1
        lo, hi = 0, m // 2
        # find largest K in [0, m//2] with max w[L..L+K-1] <= R-K+1-L
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if range_max(L, L + mid - 1) <= R - mid + 1 - L:
                lo = mid
            else:
                hi = mid - 1
        out.append(str(lo))
    sys.stdout.write("\n".join(out) + "\n")

main()