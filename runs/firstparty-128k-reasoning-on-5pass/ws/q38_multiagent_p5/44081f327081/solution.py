import sys
from math import gcd, isqrt
from itertools import islice

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    K = int(data[1])
    A = list(map(int, islice(data, 2, None)))
    del data

    w = sys.stdout.write
    CHUNK = 100000

    if K == 1:
        for i in range(0, N, CHUNK):
            w('\n'.join(map(str, A[i:i + CHUNK])) + '\n')
        return

    if K == N:
        g = 0
        for x in A:
            g = gcd(g, x)
        w((str(g) + '\n') * N)
        return

    M = max(A)
    f = [0] * (M + 1)
    for x in A:
        f[x] += 1

    is_prime = bytearray(b'\x01') * (M + 1)
    is_prime[0:2] = b'\x00\x00'
    for i in range(2, isqrt(M) + 1):
        if is_prime[i]:
            start = i * i
            is_prime[start:M + 1:i] = b'\x00' * (((M - start) // i) + 1)

    primes = [i for i in range(2, M + 1) if is_prime[i]]
    del is_prime

    for p in primes:
        for i in range(M // p, 0, -1):
            f[i] += f[i * p]

    for d in range(1, M + 1):
        f[d] = d if f[d] >= K else 0

    for p in primes:
        for i in range(1, M // p + 1):
            v = f[i]
            if v and v > f[i * p]:
                f[i * p] = v

    for i in range(0, N, CHUNK):
        w('\n'.join([str(f[x]) for x in A[i:i + CHUNK]]) + '\n')

if __name__ == '__main__':
    main()