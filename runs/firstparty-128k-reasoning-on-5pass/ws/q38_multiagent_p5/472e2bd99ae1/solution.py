import sys
from heapq import heappush, heappop, heapreplace


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]
    A = data[2:2 + N]
    B = data[2 + N:2 + 2 * N]
    C = data[2 + 2 * N:2 + 3 * N]
    del data

    if K == 1:
        a = max(A)
        b = max(B)
        c = max(C)
        print(a * b + b * c + c * a)
        return

    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    M = min(N, K)
    if M < N:
        del A[M:]
        del B[M:]
        del C[M:]

    if K == M * M * M:
        a = A[-1]
        b = B[-1]
        c = C[-1]
        print(a * b + b * c + c * a)
        return

    a0 = A[0]
    b0 = B[0]
    c0 = C[0]
    max_val = a0 * b0 + b0 * c0 + c0 * a0
    bc0 = b0 + c0

    dA = [A[i] - A[i + 1] for i in range(M - 1)]
    dB = [B[i] - B[i + 1] for i in range(M - 1)]
    dC = [C[i] - C[i + 1] for i in range(M - 1)]
    del C

    bits = max(1, (M - 1).bit_length())
    shift = bits * 3
    shift2 = bits * 2
    mask = (1 << bits) - 1
    state_mask = (1 << shift) - 1
    bit_j = 1 << bits
    bit_i = 1 << shift2
    M1 = M - 1

    heap = [0]
    push = heappush
    pop = heappop
    replace = heapreplace

    AA = A
    BB = B
    dAA = dA
    dBB = dB
    dCC = dC

    for _ in range(K - 1):
        key = heap[0]
        k = key & mask

        if k < M1:
            diff = key >> shift
            state = key & state_mask
            j = (state >> bits) & mask
            i = state >> shift2

            ai = AA[i]
            bj = BB[j]

            nd = diff + dCC[k] * (ai + bj)
            replace(heap, (nd << shift) | (state + 1))

            if k == 0:
                if j < M1:
                    nd = diff + dBB[j] * (ai + c0)
                    push(heap, (nd << shift) | (state + bit_j))
                if j == 0 and i < M1:
                    nd = diff + dAA[i] * bc0
                    push(heap, (nd << shift) | (state + bit_i))
        else:
            pop(heap)

    key = pop(heap)
    print(max_val - (key >> shift))


if __name__ == "__main__":
    solve()