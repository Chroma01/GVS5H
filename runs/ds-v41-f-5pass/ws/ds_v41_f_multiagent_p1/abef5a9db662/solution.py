import sys
from itertools import accumulate


def main():
    vals = list(map(int, sys.stdin.buffer.read().split()))
    n = vals[0]
    qpos = 1 + 2 * n
    q = vals[qpos]
    qs = vals[qpos + 1: qpos + 1 + q]

    # Only indices up to the largest queried starting rating matter.
    M = max(qs)

    # Fenwick tree over difference array D[1..M], initialized to all ones
    # (so A[X] = X initially). tr[i] = sum of D over its covered range.
    tr = [0] + [i & (-i) for i in range(1, M + 1)]
    D = [0] + [1] * M
    topbit = 1 << (M.bit_length() - 1)

    p = 1
    for _ in range(n):
        L = vals[p]
        R = vals[p + 1]
        p += 2

        # lo = first index with prefix_sum >= L
        # hi = (first index with prefix_sum >= R+1) - 1 = ii2
        # Both searches share the same descending bit sequence.
        t1 = L
        t2 = R + 1
        ii1 = 0
        ii2 = 0
        bit = topbit
        while bit:
            n1 = ii1 + bit
            if n1 <= M and tr[n1] < t1:
                ii1 = n1
                t1 -= tr[n1]
            n2 = ii2 + bit
            if n2 <= M and tr[n2] < t2:
                ii2 = n2
                t2 -= tr[n2]
            bit >>= 1

        lo = ii1 + 1
        hi = ii2
        if lo <= hi:
            D[lo] += 1
            i = lo
            while i <= M:
                tr[i] += 1
                i += i & (-i)
            if hi < M:
                D[hi + 1] -= 1
                i = hi + 1
                while i <= M:
                    tr[i] -= 1
                    i += i & (-i)

    # Recover all final ratings in one linear pass.
    A = list(accumulate(D))
    sys.stdout.write('\n'.join(str(A[x]) for x in qs) + '\n')


main()