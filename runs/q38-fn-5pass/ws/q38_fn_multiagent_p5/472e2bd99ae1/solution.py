import sys
from heapq import heappush, heappop


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]
    A = data[2:2 + N]
    B = data[2 + N:2 + 2 * N]
    C = data[2 + 2 * N:2 + 3 * N]
    del data

    # The maximum is obtained by taking the maximum of each sequence.
    if K == 1 or N == 1:
        a = max(A)
        b = max(B)
        c = max(C)
        print(a * b + b * c + c * a)
        return

    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    a0 = A[0]
    b0 = B[0]
    c0 = C[0]
    val = a0 * b0 + b0 * c0 + c0 * a0

    # Pack (i, j, k) into one integer.
    shift = (N - 1).bit_length()
    mask = (1 << shift) - 1
    i_shift = 2 * shift
    code_bits = 3 * shift
    code_mask = (1 << code_bits) - 1
    i_inc = 1 << i_shift
    j_inc = 1 << shift
    N1 = N - 1

    # Differences for O(1) value updates of children.
    dA = [A[i + 1] - A[i] for i in range(N1)]
    dB = [B[i + 1] - B[i] for i in range(N1)]
    dC = [C[i + 1] - C[i] for i in range(N1)]

    # Heap key: (-value << code_bits) + code.
    # Smaller key means larger value; ties are broken by code.
    heap = [(-val << code_bits)]

    # Spanning-tree frontier of the monotone 3D grid.
    # Unique parent:
    #   if k > 0: (i, j, k-1)
    #   elif j > 0: (i, j-1, 0)
    #   else: (i-1, 0, 0)
    # Children are the inverse moves. This avoids a visited set while
    # preserving the best-first property because every edge increases
    # exactly one index and therefore cannot increase the value.
    for _ in range(K):
        key = heappop(heap)
        code = key & code_mask
        val = -(key >> code_bits)

        k = code & mask
        j = (code >> shift) & mask
        i = code >> i_shift

        ai = A[i]

        # Child (i, j, k+1)
        if k < N1:
            nval = val + dC[k] * (ai + B[j])
            heappush(heap, (-nval << code_bits) + (code + 1))

        # Children only from the k=0 plane.
        if k == 0:
            # Child (i, j+1, 0)
            if j < N1:
                nval = val + dB[j] * (ai + c0)
                heappush(heap, (-nval << code_bits) + (code + j_inc))

            # Child (i+1, 0, 0)
            if j == 0 and i < N1:
                nval = val + dA[i] * (b0 + c0)
                heappush(heap, (-nval << code_bits) + (code + i_inc))

    print(val)


if __name__ == "__main__":
    solve()