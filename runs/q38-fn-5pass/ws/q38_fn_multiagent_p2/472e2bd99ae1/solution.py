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

    L = N if N < K else K
    if L < N:
        A = A[:L]
        B = B[:L]
        C = C[:L]

    if L == 1:
        print(A[0] * B[0] + B[0] * C[0] + C[0] * A[0])
        return

    dA = [A[i] - A[i + 1] for i in range(L - 1)]
    dB = [B[i] - B[i + 1] for i in range(L - 1)]
    dC = [C[i] - C[i + 1] for i in range(L - 1)]

    bits = (L - 1).bit_length()
    shift = 3 * bits
    mask = (1 << shift) - 1
    low_mask = (1 << bits) - 1
    two_bits = 2 * bits
    i_step = 1 << two_bits
    j_step = 1 << bits

    A0 = A[0]
    B0 = B[0]
    C0 = C[0]
    const_AB = A0 + B0
    val = A0 * B0 + B0 * C0 + C0 * A0

    heap = [-(val << shift)]

    A_list = A
    B_list = B
    C_list = C
    dA_list = dA
    dB_list = dB
    dC_list = dC
    Lm1 = L - 1

    push = heappush
    pop = heappop
    replace = heapreplace

    for _ in range(K - 1):
        key = heap[0]
        t = -key
        val = t >> shift
        code = t & mask

        k = code & low_mask
        j = (code >> bits) & low_mask
        i = code >> two_bits

        if i < Lm1:
            Ck = C_list[k]

            nval = val - dA_list[i] * (B_list[j] + Ck)
            child_key = -(nval << shift) - (code + i_step)
            replace(heap, child_key)

            if i == 0:
                if j < Lm1:
                    nval = val - dB_list[j] * (A0 + Ck)
                    push(heap, -(nval << shift) - (code + j_step))

                if j == 0 and k < Lm1:
                    nval = val - dC_list[k] * const_AB
                    push(heap, -(nval << shift) - (code + 1))
        else:
            pop(heap)

    print((-heap[0]) >> shift)


if __name__ == "__main__":
    solve()