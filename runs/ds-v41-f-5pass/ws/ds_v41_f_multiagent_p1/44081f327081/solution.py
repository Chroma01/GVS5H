import sys
from math import gcd
from array import array


def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); K = int(data[1])
    it = iter(data)
    next(it); next(it)
    A = array('i', map(int, it))
    del data, it
    out = sys.stdout
    CH = 1 << 16

    # K == 1: answer is A_i itself
    if K == 1:
        buf = []
        for a in A:
            buf.append(str(a))
            if len(buf) >= CH:
                out.write('\n'.join(buf)); out.write('\n'); buf.clear()
        if buf:
            out.write('\n'.join(buf)); out.write('\n')
        return

    # K == N: answer is gcd of all elements
    if K == N:
        g = 0
        for v in A:
            g = gcd(g, v)
        out.write(('%d\n' % g) * N)
        return

    M = max(A)

    # frequency of each value
    freq = [0] * (M + 1)
    for v in A:
        freq[v] += 1

    # cnt[d] = number of array elements divisible by d (with multiplicity)
    cnt = [0] * (M + 1)
    for d in range(1, M + 1):
        cnt[d] = sum(freq[d::d])
    del freq

    # best[x] = largest divisor d of x with cnt[d] >= K
    # iterate d ascending and overwrite multiples; the last (largest) d wins
    best = [0] * (M + 1)
    for d in range(1, M + 1):
        if cnt[d] >= K:
            best[d::d] = [d] * (M // d)
    del cnt

    get = best.__getitem__
    buf = []
    for a in A:
        buf.append(str(get(a)))
        if len(buf) >= CH:
            out.write('\n'.join(buf)); out.write('\n'); buf.clear()
    if buf:
        out.write('\n'.join(buf)); out.write('\n')


main()