import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0
    N = data[p]; p += 1
    A = data[p:p + N]; p += N
    B = data[p:p + N]; p += N
    K = data[p]; p += 1
    xs = [0] * K
    ys = [0] * K
    for k in range(K):
        xs[k] = data[p] - 1
        ys[k] = data[p + 1] - 1
        p += 2

    # ---- coordinate compression (1-based for Fenwick) ----
    vals = sorted(set(A) | set(B))
    comp = {v: i + 1 for i, v in enumerate(vals)}
    M = len(vals)
    ca = [comp[v] for v in A]
    cb = [comp[v] for v in B]

    # ---- Hilbert order for the (X, Y) query points ----
    POW = 1
    while (1 << POW) < N:
        POW += 1

    def hilbertOrder(x, y):
        d = 0
        s = 1 << (POW - 1)
        while s:
            rx = 1 if (x & s) else 0
            ry = 1 if (y & s) else 0
            d = (d << 2) | (rx * 3 ^ ry)
            if ry == 0:
                if rx:
                    x = s - 1 - x
                    y = s - 1 - y
                x, y = y, x
            s >>= 1
        return d

    order = sorted(range(K), key=lambda k: hilbertOrder(xs[k], ys[k]))

    # ---- Packed Fenwick trees ----
    # Each tree entry packs (count << SHIFT) | sum of the active multiset.
    # sum <= 1e5 * 2e8 = 2e13 < 2^45, count <= 1e5 < 2^17, so packing is exact.
    # This halves the inner-loop work versus separate count/sum trees.
    SHIFT = 45
    MASK = (1 << SHIFT) - 1
    ONE = 1 << SHIFT

    bitA = [0] * (M + 1)   # packed count/sum of active A prefix
    bitB = [0] * (M + 1)   # packed count/sum of active B prefix

    packA = [ONE + a for a in A]   # per-index packed update deltas
    packB = [ONE + b for b in B]

    ans = [0] * K
    cur = 0
    cntA = 0; sumA = 0
    cntB = 0; sumB = 0
    cx = 0  # active prefix length of A
    cy = 0  # active prefix length of B

    # Delta of element v against opposite set S:
    #   sum_{u in S} |v-u| = v*(2*cntLe(v) - cntTotal) + (sumTotal - 2*sumLe(v))
    # computed against the opposite tree BEFORE modifying the element's own tree.
    for k in order:
        tx = xs[k] + 1
        ty = ys[k] + 1

        while cx < tx:                      # add A[cx]
            v = ca[cx]; a = A[cx]
            if cntB:
                i = v; pk = 0
                while i:
                    pk += bitB[i]
                    i -= i & -i
                cur += a * (2 * (pk >> SHIFT) - cntB) + (sumB - 2 * (pk & MASK))
            d = packA[cx]; i = v
            while i <= M:
                bitA[i] += d
                i += i & -i
            cntA += 1; sumA += a
            cx += 1
        while cx > tx:                      # remove A[cx-1]
            cx -= 1
            v = ca[cx]; a = A[cx]
            if cntB:
                i = v; pk = 0
                while i:
                    pk += bitB[i]
                    i -= i & -i
                cur -= a * (2 * (pk >> SHIFT) - cntB) + (sumB - 2 * (pk & MASK))
            d = -packA[cx]; i = v
            while i <= M:
                bitA[i] += d
                i += i & -i
            cntA -= 1; sumA -= a

        while cy < ty:                      # add B[cy]
            v = cb[cy]; b = B[cy]
            if cntA:
                i = v; pk = 0
                while i:
                    pk += bitA[i]
                    i -= i & -i
                cur += b * (2 * (pk >> SHIFT) - cntA) + (sumA - 2 * (pk & MASK))
            d = packB[cy]; i = v
            while i <= M:
                bitB[i] += d
                i += i & -i
            cntB += 1; sumB += b
            cy += 1
        while cy > ty:                      # remove B[cy-1]
            cy -= 1
            v = cb[cy]; b = B[cy]
            if cntA:
                i = v; pk = 0
                while i:
                    pk += bitA[i]
                    i -= i & -i
                cur -= b * (2 * (pk >> SHIFT) - cntA) + (sumA - 2 * (pk & MASK))
            d = -packB[cy]; i = v
            while i <= M:
                bitB[i] += d
                i += i & -i
            cntB -= 1; sumB -= b

        ans[k] = cur

    sys.stdout.write('\n'.join(map(str, ans)) + '\n')


main()