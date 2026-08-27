import sys
from math import gcd, isqrt
from itertools import islice


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    K = int(data[1])

    if K == 1:
        write = sys.stdout.buffer.write
        chunk = 10000
        end = 2 + N
        for i in range(2, end, chunk):
            write(b'\n'.join(data[i:i + chunk]) + b'\n')
        return

    if K == N:
        g = 0
        end = 2 + N
        gcd_func = gcd
        for i in range(2, end):
            g = gcd_func(g, int(data[i]))
            if g == 1:
                break
        del data
        sys.stdout.buffer.write((str(g).encode() + b'\n') * N)
        return

    A = list(map(int, islice(data, 2, 2 + N)))
    del data

    M = max(A)
    if M == 1:
        sys.stdout.buffer.write(b'1\n' * N)
        return

    b = [0] * (M + 1)
    for x in A:
        b[x] += 1

    limit = M // 2
    if limit >= 2:
        sieve = bytearray(b'\x01') * (limit + 1)
        sieve[0:2] = b'\x00\x00'
        r = isqrt(limit)
        for i in range(2, r + 1):
            if sieve[i]:
                start = i * i
                sieve[start:limit + 1:i] = b'\x00' * (((limit - start) // i) + 1)
        primes = [i for i in range(2, limit + 1) if sieve[i]]
        del sieve
    else:
        primes = []

    for p in primes:
        mp = M // p
        y = mp * p
        for x in range(mp, 0, -1):
            b[x] += b[y]
            y -= p

    b[1] = N

    for d in range(1, M + 1):
        b[d] = d if b[d] >= K else 1

    for p in primes:
        mp = M // p
        y = p
        for x in range(1, mp + 1):
            if b[x] > b[y]:
                b[y] = b[x]
            y += p

    del primes

    write = sys.stdout.write
    out = []
    append = out.append
    cnt = 0
    chunk = 10000
    for x in A:
        append(str(b[x]))
        cnt += 1
        if cnt == chunk:
            write('\n'.join(out))
            write('\n')
            out.clear()
            cnt = 0
    if out:
        write('\n'.join(out))
        write('\n')


if __name__ == '__main__':
    main()