import sys
from math import gcd
from functools import reduce


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = list(map(int, it))
    del data, it

    n = len(A)

    if K == 1:
        write = sys.stdout.write
        chunk_size = 100000
        for i in range(0, n, chunk_size):
            chunk = A[i:i + chunk_size]
            write('\n'.join(map(str, chunk)))
            if i + chunk_size < n:
                write('\n')
        return

    if K == N:
        g = reduce(gcd, A)
        sys.stdout.write((str(g) + '\n') * n)
        return

    M = max(A)

    freq = [0] * (M + 1)
    for x in A:
        freq[x] += 1

    ans = [1] * (M + 1)

    f = freq
    a = ans
    k = K
    M1 = M + 1

    # Small divisors: use C-level slicing for most of the harmonic work.
    B = min(M, max(1000, M // 100))
    sum_ = sum

    for d in range(2, B + 1):
        if f[d] >= k or sum_(f[d::d]) >= k:
            n_mult = (M - d) // d + 1
            a[d::d] = [d] * n_mult

    # Large divisors: Python loops, with unrolled tails.
    start = B + 1
    if start <= M:
        quarter = M // 4
        third = M // 3
        half = M // 2

        # General region: at least 4 multiples.
        end = quarter
        if start <= end:
            for d in range(start, end + 1):
                s = f[d]
                if s >= k:
                    for j in range(d, M1, d):
                        a[j] = d
                    continue

                for j in range(d + d, M1, d):
                    s += f[j]
                    if s >= k:
                        for j in range(d, M1, d):
                            a[j] = d
                        break

        # At most 3 multiples.
        l = quarter + 1
        if l < start:
            l = start
        r = third
        if l <= r:
            for d in range(l, r + 1):
                s = f[d] + f[d + d] + f[d + d + d]
                if s >= k:
                    a[d] = d
                    a[d + d] = d
                    a[d + d + d] = d

        # At most 2 multiples.
        l = third + 1
        if l < start:
            l = start
        r = half
        if l <= r:
            for d in range(l, r + 1):
                s = f[d] + f[d + d]
                if s >= k:
                    a[d] = d
                    a[d + d] = d

        # At most 1 multiple.
        l = half + 1
        if l < start:
            l = start
        if l <= M:
            for d in range(l, M1):
                if f[d] >= k:
                    a[d] = d

    del f, freq

    write = sys.stdout.write
    chunk_size = 100000
    for i in range(0, n, chunk_size):
        chunk = A[i:i + chunk_size]
        write('\n'.join([str(a[x]) for x in chunk]))
        if i + chunk_size < n:
            write('\n')


if __name__ == "__main__":
    main()