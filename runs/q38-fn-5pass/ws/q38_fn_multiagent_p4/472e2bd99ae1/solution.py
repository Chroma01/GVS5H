import sys
from heapq import heappush, heappop


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

    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    L = N if N < K else K
    if L < N:
        A = A[:L]
        B = B[:L]
        C = C[:L]

    # Adjacent differences for fast value updates.
    dA = [A[i + 1] - A[i] for i in range(L - 1)]
    dB = [B[i + 1] - B[i] for i in range(L - 1)]
    dC = [C[i + 1] - C[i] for i in range(L - 1)]

    # Encode (i, j, k) into one integer using fixed-width bit fields.
    BITS = max(1, (L - 1).bit_length())
    MASK = (1 << BITS) - 1
    SHIFT = 3 * BITS
    CODE_MASK = (1 << SHIFT) - 1
    SHIFT2 = 2 * BITS
    I_STEP = 1 << SHIFT2
    J_STEP = 1 << BITS
    Lm1 = L - 1

    ai = A[0]
    bj = B[0]
    ck = C[0]
    root_val = ai * bj + bj * ck + ck * ai

    # Pack (value, code) into one integer:
    # key = (-value << SHIFT) + code.
    # Python's min-heap then pops largest value first; ties use smaller code.
    heap = [((-root_val) << SHIFT)]
    visited = {0}

    push = heappush
    pop = heappop
    visited_add = visited.add

    for _ in range(K - 1):
        key = pop(heap)
        val = -(key >> SHIFT)
        code = key & CODE_MASK

        k_idx = code & MASK
        j_idx = (code >> BITS) & MASK
        i_idx = code >> SHIFT2

        ai = A[i_idx]
        bj = B[j_idx]
        ck = C[k_idx]

        if i_idx < Lm1:
            ncode = code + I_STEP
            if ncode not in visited:
                visited_add(ncode)
                nval = val + dA[i_idx] * (bj + ck)
                push(heap, ((-nval) << SHIFT) + ncode)

        if j_idx < Lm1:
            ncode = code + J_STEP
            if ncode not in visited:
                visited_add(ncode)
                nval = val + dB[j_idx] * (ai + ck)
                push(heap, ((-nval) << SHIFT) + ncode)

        if k_idx < Lm1:
            ncode = code + 1
            if ncode not in visited:
                visited_add(ncode)
                nval = val + dC[k_idx] * (ai + bj)
                push(heap, ((-nval) << SHIFT) + ncode)

    key = pop(heap)
    sys.stdout.write(str(-(key >> SHIFT)) + "\n")


if __name__ == "__main__":
    main()