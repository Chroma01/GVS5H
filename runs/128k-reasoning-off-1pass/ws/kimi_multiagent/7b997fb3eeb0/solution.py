import sys


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    N = int(data[p]); p += 1
    A = [int(x) for x in data[p:p + N]]; p += N

    INF = N  # legit w[i] <= N-1; bound m-K <= N-1, so INF always fails '<='

    # nxt[i] = first index j with A[j] >= 2*A[i] (two pointers, O(N))
    # w[i] = nxt[i] - i, or INF if no such j
    w = [0] * N
    j = 0
    for i in range(N):
        ai2 = A[i] * 2
        if j <= i:
            j = i + 1
        while j < N and A[j] < ai2:
            j += 1
        w[i] = j - i if j < N else INF

    # Sparse table for range max over w
    st = [w]
    k = 1
    while (1 << k) <= N:
        prev = st[k - 1]
        half = 1 << (k - 1)
        st.append([max(a, b) for a, b in zip(prev, prev[half:])])
        k += 1

    Q = int(data[p]); p += 1
    out = []
    append = out.append
    st_local = st

    for _ in range(Q):
        L = int(data[p]) - 1
        R = int(data[p + 1]) - 1
        p += 2
        m = R - L + 1
        limit = m >> 1
        K = 0
        cur = 0  # running max of w over [L, L+K-1]; w >= 1 so 0 acts as -inf
        # Binary lifting: find max K <= m//2 with max(w[L..L+K-1]) <= m-K
        for b in range(17, -1, -1):
            nk = K + (1 << b)
            if nk <= limit:
                v = st_local[b][L + K]  # max over the new segment [L+K, L+K+2^b-1]
                cand = cur if cur >= v else v
                if cand <= m - nk:
                    K = nk
                    cur = cand
        append(str(K))

    sys.stdout.write("\n".join(out) + "\n")


main()