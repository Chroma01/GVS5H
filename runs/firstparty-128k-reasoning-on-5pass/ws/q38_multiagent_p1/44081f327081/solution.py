import sys
from math import gcd, isqrt


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))
    K = int(next(it))

    # K = 1: the chosen set is just A_i itself.
    if K == 1:
        out = sys.stdout.buffer
        write = out.write
        chunk = 100000
        end_all = 2 + N
        for i in range(2, end_all, chunk):
            end = i + chunk
            if end > end_all:
                end = end_all
            write(b'\n'.join(data[i:end]) + b'\n')
        return

    # K = N: all elements must be chosen, so the answer is gcd(A).
    if K == N:
        g = 0
        for b in it:
            g = gcd(g, int(b))
            if g == 1:
                break
        sys.stdout.buffer.write((str(g) + '\n').encode() * N)
        return

    A = list(map(int, it))
    del it
    del data

    maxA = max(A)

    # All values are 1, so every answer is 1.
    if maxA == 1:
        sys.stdout.buffer.write(b'1\n' * N)
        return

    freq = [0] * (maxA + 1)
    for x in A:
        freq[x] += 1

    # Sieve primes up to maxA.
    is_prime = bytearray(b'\x01') * (maxA + 1)
    is_prime[0:2] = b'\x00\x00'
    r = isqrt(maxA)
    for i in range(2, r + 1):
        if is_prime[i]:
            start = i * i
            is_prime[start:maxA + 1:i] = b'\x00' * (((maxA - start) // i) + 1)

    primes = [i for i in range(2, maxA + 1) if is_prime[i]]
    del is_prime

    f = freq
    M = maxA

    # Zeta transform over divisibility:
    # after this, f[d] = number of array elements divisible by d.
    for p in primes:
        limit = M // p
        for d in range(limit, 0, -1):
            f[d] += f[d * p]

    # Keep only divisors that can be the GCD of K chosen elements.
    for d in range(1, M + 1):
        c = f[d]
        if c >= K:
            f[d] = d
        else:
            f[d] = 0

    # Max-zeta transform over divisibility:
    # after this, f[x] = max valid divisor of x.
    for p in primes:
        limit = M // p
        for d in range(1, limit + 1):
            v = f[d]
            if v:
                t = d * p
                if v > f[t]:
                    f[t] = v

    del primes

    out = sys.stdout.buffer
    write = out.write
    to_str = str
    chunk = 100000

    for i in range(0, N, chunk):
        end = i + chunk
        if end > N:
            end = N
        lines = [to_str(f[x]) for x in A[i:end]]
        write(('\n'.join(lines) + '\n').encode())


if __name__ == '__main__':
    main()