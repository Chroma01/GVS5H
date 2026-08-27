import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    A = [0] * (N + 1)  # 1-based
    for i in range(1, N + 1):
        A[i] = int(data[pos]); pos += 1
    Q = int(data[pos]); pos += 1
    queries = []
    for _ in range(Q):
        L = int(data[pos]); R = int(data[pos + 1]); pos += 2
        queries.append((L, R))

    INF = N + 5
    # nxt[i] = smallest index j with A[j] >= 2*A[i]; M[i] = nxt[i] - i (INF if none)
    M = [0] * (N + 1)
    for i in range(1, N + 1):
        j = bisect_left(A, 2 * A[i], i + 1, N + 1)
        if j > N:
            M[i] = INF
        else:
            M[i] = j - i

    # Sparse table for range maximum of M[1..N]
    LOG = max(1, (N).bit_length())
    st = [M[:]]
    length = 1
    while length * 2 <= N:
        prev = st[-1]
        cur = [0] * (N + 1)
        for i in range(1, N - 2 * length + 2):
            a = prev[i]
            b = prev[i + length]
            cur[i] = a if a >= b else b
        st.append(cur)
        length *= 2

    log2 = [0] * (N + 2)
    for i in range(2, N + 2):
        log2[i] = log2[i >> 1] + 1

    def range_max(l, r):
        k = log2[r - l + 1]
        row = st[k]
        a = row[l]
        b = row[r - (1 << k) + 1]
        return a if a >= b else b

    out = []
    for (L, R) in queries:
        length_q = R - L + 1
        lo, hi = 0, length_q // 2
        # find max K such that range_max(L, L+K-1) <= length_q - K
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if range_max(L, L + mid - 1) <= length_q - mid:
                lo = mid
            else:
                hi = mid - 1
        out.append(str(lo))

    sys.stdout.write("\n".join(out) + "\n")

main()