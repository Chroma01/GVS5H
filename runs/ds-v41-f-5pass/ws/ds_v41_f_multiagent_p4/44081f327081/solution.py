import sys
from array import array
from math import gcd, isqrt


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = array('I', map(int, it))
    del data, it

    out = sys.stdout.write

    # K == 1 : the subset is just {A_i}, answer = A_i
    if K == 1:
        buf = []
        ap = buf.append
        for x in A:
            ap(str(x))
            if len(buf) >= 16384:
                out('\n'.join(buf) + '\n')
                buf.clear()
        if buf:
            out('\n'.join(buf) + '\n')
        return

    # K == N : must take the whole array
    if K == N:
        g = 0
        for x in A:
            g = gcd(g, x)
        out((str(g) + '\n') * N)
        return

    M = max(A)

    freq = [0] * (M + 1)
    for x in A:
        freq[x] += 1

    half = M >> 1

    # primes up to M (bytearray sieve)
    sieve = bytearray([1]) * (M + 1)
    sieve[0] = 0
    sieve[1] = 0
    for i in range(2, isqrt(M) + 1):
        if sieve[i]:
            st = i * i
            sieve[st::i] = bytes((M - st) // i + 1)
    primes = [i for i in range(2, M + 1) if sieve[i]]
    del sieve

    # f[x] = largest divisor d of x with (# elements of A divisible by d) >= K
    fr = freq
    f = [1] * (M + 1)
    for x in range(2, M + 1):
        if x <= half:
            # x has more than one multiple in [1, M]
            if sum(fr[x::x]) >= K:
                f[x] = x
                fx = x
            else:
                fx = f[x]
            if fx != 1:
                lim = M // x
                for p in primes:
                    if p > lim:
                        break
                    y = p * x
                    if f[y] < fx:
                        f[y] = fx
        else:
            # the only multiple of x in [1, M] is x itself
            if fr[x] >= K:
                f[x] = x

    buf = []
    ap = buf.append
    for x in A:
        ap(str(f[x]))
        if len(buf) >= 16384:
            out('\n'.join(buf) + '\n')
            buf.clear()
    if buf:
        out('\n'.join(buf) + '\n')


main()