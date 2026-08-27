import sys
from heapq import heappush, heappop, heapify


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    K = data[1]
    A = data[2:2 + N]
    B = data[2 + N:2 + 2 * N]
    C = data[2 + 2 * N:2 + 3 * N]
    del data

    if K == 1:
        a = max(A)
        b = max(B)
        c = max(C)
        sys.stdout.write(str(a * b + b * c + c * a) + '\n')
        return

    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    m = N if N < K else K
    if m < N:
        A = A[:m]
        B = B[:m]
        C = C[:m]

    a0 = A[0]
    b0 = B[0]
    c0 = C[0]
    root = a0 * b0 + b0 * c0 + c0 * a0

    ca = 0
    while ca < m and A[ca] == a0:
        ca += 1
    cb = 0
    while cb < m and B[cb] == b0:
        cb += 1
    cc = 0
    while cc < m and C[cc] == c0:
        cc += 1
    if ca * cb * cc >= K:
        sys.stdout.write(str(root) + '\n')
        return

    if K >= m * m * m:
        ai = A[-1]
        bj = B[-1]
        ck = C[-1]
        sys.stdout.write(str(ai * bj + bj * ck + ck * ai) + '\n')
        return

    # Choose axis order.  The value xy + yz + zx is symmetric in the three
    # arrays, so any permutation is safe.  The i-axis is expanded most often,
    # so put the smallest primary-axis drop first.
    dropA = (A[0] - A[1]) * (B[0] + C[0])
    dropB = (B[0] - B[1]) * (C[0] + A[0])
    dropC = (C[0] - C[1]) * (A[0] + B[0])
    order = [(dropA, A), (dropB, B), (dropC, C)]
    order.sort(key=lambda x: x[0])
    A, B, C = order[0][1], order[1][1], order[2][1]
    del order

    a0 = A[0]
    b0 = B[0]
    c0 = C[0]
    root = a0 * b0 + b0 * c0 + c0 * a0

    shift = max(1, (m - 1).bit_length())
    total = 3 * shift
    mask = (1 << shift) - 1
    code_mask = (1 << total) - 1
    shift2 = 2 * shift
    j_inc = 1 << shift
    k_inc = 1 << shift2
    m1 = m - 1

    Adiff = [A[i] - A[i + 1] for i in range(m1)]
    Bdiff = [B[i] - B[i + 1] for i in range(m1)]
    Cdiff = [C[i] - C[i + 1] for i in range(m1)]
    del A

    Ad = Adiff
    Bd = Bdiff
    Cd = Cdiff
    Ad0 = Ad[0]
    Bd0 = Bd[0]
    Cd0 = Cd[0]
    sum0 = a0 + b0
    a0_plus_C = [a0 + c for c in C]

    B_loc = B
    C_loc = C
    heappop_loc = heappop
    heappush_loc = heappush
    heapify_loc = heapify

    # Root is already counted.  Start from its three children.
    heap = [
        ((Ad0 * (b0 + c0)) << total) | 1,
        ((Bd0 * a0_plus_C[0]) << total) | j_inc,
        ((Cd0 * sum0) << total) | k_inc,
    ]
    heapify_loc(heap)

    for _ in range(K - 2):
        key = heappop_loc(heap)
        delta = key >> total
        code = key & code_mask
        i = code & mask

        if i:
            if i < m1:
                j = (code >> shift) & mask
                k = code >> shift2
                delta += Ad[i] * (B_loc[j] + C_loc[k])
                heappush_loc(heap, (delta << total) | (code + 1))
            continue

        j = (code >> shift) & mask
        k = code >> shift2
        bj = B_loc[j]
        ck = C_loc[k]
        ack = a0_plus_C[k]

        delta_i = delta + Ad0 * (bj + ck)
        heappush_loc(heap, (delta_i << total) | (code + 1))

        if j:
            if j < m1:
                delta_j = delta + Bd[j] * ack
                heappush_loc(heap, (delta_j << total) | (code + j_inc))
        else:
            delta_j = delta + Bd0 * ack
            heappush_loc(heap, (delta_j << total) | (code + j_inc))
            if k < m1:
                delta_k = delta + Cd[k] * sum0
                heappush_loc(heap, (delta_k << total) | (code + k_inc))

    ans = root - (heap[0] >> total)
    sys.stdout.write(str(ans) + '\n')


if __name__ == "__main__":
    main()