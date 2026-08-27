import sys
from math import gcd, isqrt


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    out = sys.stdout.buffer

    # If only one element is chosen, the gcd is the element itself.
    if K == 1:
        out.write(b'\n'.join(it))
        out.write(b'\n')
        return

    # If all elements must be chosen, the answer is the gcd of the whole array.
    if K == N:
        g = 0
        for tok in it:
            g = gcd(g, int(tok))
            if g == 1:
                break

        del data, it

        # Print the same answer on N separate lines.
        line = (str(g) + '\n').encode()
        chunk = 100000
        for start in range(0, N, chunk):
            out.write(line * min(chunk, N - start))
        return

    A = list(map(int, it))
    del data, it

    M = max(A)
    f = [0] * (M + 1)

    # Frequency of each value.
    for x in A:
        f[x] += 1

    # Sieve primes up to M.
    if M >= 2:
        is_prime = bytearray(b'\x01') * (M + 1)
        is_prime[0:2] = b'\x00\x00'
        r = isqrt(M)
        for i in range(2, r + 1):
            if is_prime[i]:
                start = i * i
                is_prime[start:M + 1:i] = b'\x00' * (((M - start) // i) + 1)
        primes = [i for i in range(2, M + 1) if is_prime[i]]
        del is_prime
    else:
        primes = []

    # Multiple-count zeta transform:
    # after this, f[d] = number of array elements divisible by d.
    for p in primes:
        limit = M // p
        j = limit * p
        for d in range(limit, 0, -1):
            f[d] += f[j]
            j -= p

    # Keep only valid divisors: d is valid iff at least K elements are divisible by d.
    for d in range(1, M + 1):
        if f[d] >= K:
            f[d] = d
        else:
            f[d] = 0

    # Max-over-divisors zeta transform:
    # after this, f[x] = maximum valid divisor of x.
    for p in primes:
        limit = M // p
        j = p
        for d in range(1, limit + 1):
            v = f[d]
            if v > f[j]:
                f[j] = v
            j += p

    del primes

    # Chunked output.
    write = out.write
    chunk = 100000
    for i in range(0, N, chunk):
        part = A[i:i + chunk]
        write(('\n'.join([str(f[x]) for x in part])).encode())
        write(b'\n')


if __name__ == '__main__':
    main()