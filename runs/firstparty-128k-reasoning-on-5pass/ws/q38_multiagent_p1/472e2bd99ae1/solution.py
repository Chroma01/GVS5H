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

    M = min(N, K)
    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)
    if M < N:
        A = A[:M]
        B = B[:M]
        C = C[:M]

    arrs = [A, B, C]
    arrs.sort(key=lambda x: x[0] - x[-1], reverse=True)
    X, Y, Z = arrs
    del A, B, C, arrs

    Xl, Yl, Zl = X, Y, Z
    del X, Y, Z

    bits = max(1, (M - 1).bit_length())
    shift = 3 * bits
    shift_i = 2 * bits
    mask = (1 << bits) - 1
    low_mask = (1 << shift) - 1
    Mi1 = M - 1

    dX = [0] * Mi1
    dY = [0] * Mi1
    dZ = [0] * Mi1
    for i in range(Mi1):
        dX[i] = Xl[i + 1] - Xl[i]
        dY[i] = Yl[i + 1] - Yl[i]
        dZ[i] = Zl[i + 1] - Zl[i]

    Z0 = Zl[0]
    const_i = Yl[0] + Z0
    Xpz = [x + Z0 for x in Xl]
    del Zl

    root_val = Xl[0] * (Yl[0] + Z0) + Yl[0] * Z0
    heap = [(-root_val << shift)]

    hp = heappush
    hpop = heappop
    hreplace = heapreplace
    out = sys.stdout.write

    shift_l = shift
    shift_i_l = shift_i
    bits_l = bits
    mask_l = mask
    low_mask_l = low_mask
    Mi1_l = Mi1
    const_i_l = const_i
    dXl = dX
    dYl = dY
    dZl = dZ
    Xpzl = Xpz

    for _ in range(K - 1):
        key = heap[0]
        val = -(key >> shift_l)
        idx = key & low_mask_l
        i = idx >> shift_i_l
        j = (idx >> bits_l) & mask_l
        k = idx & mask_l

        x = Xl[i]
        y = Yl[j]
        i_part = i << shift_i_l
        j_part = j << bits_l

        c1 = None
        c2 = None
        c3 = None

        if k == 0:
            if j < Mi1_l:
                nv = val + dYl[j] * Xpzl[i]
                c1 = (-nv << shift_l) + (i_part | ((j + 1) << bits_l))
            if j == 0 and i < Mi1_l:
                nv = val + dXl[i] * const_i_l
                c2 = (-nv << shift_l) + ((i + 1) << shift_i_l)

        if k < Mi1_l:
            nv = val + dZl[k] * (x + y)
            c3 = (-nv << shift_l) + (i_part | j_part | (k + 1))

        first = None
        if c1 is not None:
            first = c1
        if c2 is not None:
            if first is None or c2 < first:
                first = c2
        if c3 is not None:
            if first is None or c3 < first:
                first = c3

        if first is not None:
            hreplace(heap, first)
            if c1 is not None and c1 is not first:
                hp(heap, c1)
            if c2 is not None and c2 is not first:
                hp(heap, c2)
            if c3 is not None and c3 is not first:
                hp(heap, c3)
        else:
            hpop(heap)

    ans = -(heap[0] >> shift_l)
    out(str(ans) + '\n')

if __name__ == "__main__":
    solve()