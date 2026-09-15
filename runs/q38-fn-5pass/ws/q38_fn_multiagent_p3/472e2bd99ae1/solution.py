import sys
import heapq


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    K = int(data[1])

    A = list(map(int, data[2:2 + N]))
    B = list(map(int, data[2 + N:2 + 2 * N]))
    C = list(map(int, data[2 + 2 * N:2 + 3 * N]))
    del data

    # The maximum is obtained by taking the maximum of each sequence.
    if K == 1:
        a = max(A)
        b = max(B)
        c = max(C)
        print(a * b + b * c + c * a)
        return

    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    # It is safe to keep only the first K elements of each sorted array.
    M = N if N < K else K
    if M < N:
        del A[M:]
        del B[M:]
        del C[M:]

    # If the remaining relevant part is constant, every top value is the same.
    if A[0] == A[-1] and B[0] == B[-1] and C[0] == C[-1]:
        a = A[0]
        b = B[0]
        c = C[0]
        print(a * b + b * c + c * a)
        return

    m = M
    mm = m * m
    m1 = m - 1

    # Pack heap entries into one integer:
    # item = (negative_value << shift) + key
    # key = (i * m + j) * m + k, and key < 2**shift.
    shift = (mm * m - 1).bit_length()
    mask = (1 << shift) - 1

    a0 = A[0]
    b0 = B[0]
    c0 = C[0]
    init_neg = -(a0 * b0 + b0 * c0 + c0 * a0)

    heap = [(init_neg << shift)]
    visited = {0}

    heappop = heapq.heappop
    heappush = heapq.heappush
    divmod_ = divmod

    vis = visited
    vis_add = vis.add
    AA = A
    BB = B
    CC = C
    sh = shift
    mk = mask

    # Pop the first K-1 triples. The next heap top is the K-th largest value.
    for _ in range(K - 1):
        item = heappop(heap)
        key = item & mk
        neg = item >> sh

        i, rem = divmod_(key, mm)
        j, k = divmod_(rem, m)

        ai = AA[i]
        bj = BB[j]
        ck = CC[k]

        if i < m1:
            nkey = key + mm
            if nkey not in vis:
                vis_add(nkey)
                new_neg = neg - (AA[i + 1] - ai) * (bj + ck)
                heappush(heap, (new_neg << sh) + nkey)

        if j < m1:
            nkey = key + m
            if nkey not in vis:
                vis_add(nkey)
                new_neg = neg - (BB[j + 1] - bj) * (ai + ck)
                heappush(heap, (new_neg << sh) + nkey)

        if k < m1:
            nkey = key + 1
            if nkey not in vis:
                vis_add(nkey)
                new_neg = neg - (CC[k + 1] - ck) * (ai + bj)
                heappush(heap, (new_neg << sh) + nkey)

    print(-(heap[0] >> sh))


if __name__ == "__main__":
    solve()