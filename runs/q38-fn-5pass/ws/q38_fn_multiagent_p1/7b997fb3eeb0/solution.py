import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    idx = 0
    N = data[idx]
    idx += 1

    A = data[idx:idx + N]
    idx += N

    Q = data[idx]
    idx += 1

    # B[i] = f(i) - i, where f(i) is the first index j with A[j] >= 2*A[i].
    # If no such j exists, use f(i) = N, so B[i] = N - i.
    B = [0] * N
    j = 0
    for i in range(N):
        if j < i + 1:
            j = i + 1
        target = A[i] << 1
        while j < N and A[j] < target:
            j += 1
        B[i] = j - i

    # Keep only queries, then release the large input/A lists early.
    queries = data[idx:]
    del data, A

    # logs[x] = floor(log2(x))
    logs = [0] * (N + 1)
    for i in range(2, N + 1):
        logs[i] = logs[i >> 1] + 1

    # Sparse table for range maximum queries on B.
    st = [B]
    step = 1
    while (step << 1) <= N:
        prev = st[-1]
        st.append([x if x >= y else y for x, y in zip(prev, prev[step:])])
        step <<= 1

    pow2 = [1 << i for i in range(len(st))]

    out = []
    append = out.append

    logs_l = logs
    st_l = st
    pow2_l = pow2
    d = queries
    idx = 0

    for _ in range(Q):
        L = d[idx] - 1
        R = d[idx + 1] - 1
        idx += 2

        m = R - L + 1
        lo = 0
        hi = m >> 1

        # Binary search the maximum feasible k.
        while lo < hi:
            mid = (lo + hi + 1) >> 1

            # Range maximum of B[L .. L+mid-1].
            kk = logs_l[mid]
            row = st_l[kk]
            pp = pow2_l[kk]
            threshold = m - mid

            # max of two overlapping blocks <= threshold iff both blocks <= threshold.
            if row[L] <= threshold and row[L + mid - pp] <= threshold:
                lo = mid
            else:
                hi = mid - 1

        append(str(lo))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()