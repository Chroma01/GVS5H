import sys
from array import array
from math import isqrt


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    _ = int(next(it))  # N, not needed explicitly
    K = int(next(it))

    # Store the original sequence compactly.
    A = array('I', map(int, it))
    del data, it

    if not A:
        return

    M = max(A)
    freq = [0] * (M + 1)

    for x in A:
        freq[x] += 1

    # Sieve primes up to M.
    if M >= 2:
        sieve = bytearray(b'\x01') * (M + 1)
        sieve[0] = 0
        sieve[1] = 0
        limit = isqrt(M)
        for i in range(2, limit + 1):
            if sieve[i]:
                start = i * i
                sieve[start:M + 1:i] = b'\x00' * (((M - start) // i) + 1)
        primes = [i for i in range(2, M + 1) if sieve[i]]
        del sieve
    else:
        primes = []

    f = freq

    # Counting transform:
    # After this, f[d] = number of array elements divisible by d.
    for p in primes:
        mp = M // p
        for d in range(mp, 0, -1):
            f[d] += f[d * p]

    # Keep only feasible divisors.
    for d in range(1, M + 1):
        c = f[d]
        f[d] = d if c >= K else 0

    # Max-propagation transform:
    # After this, f[x] = maximum feasible divisor of x.
    for p in primes:
        mp = M // p
        for d in range(1, mp + 1):
            v = f[d]
            if v:
                j = d * p
                if v > f[j]:
                    f[j] = v

    del primes

    # Chunked output.
    write = sys.stdout.buffer.write
    join = '\n'.join
    buf = []
    CH = 20000

    for x in A:
        buf.append(str(f[x]))
        if len(buf) >= CH:
            write((join(buf) + '\n').encode())
            buf = []

    if buf:
        write((join(buf) + '\n').encode())


if __name__ == '__main__':
    main()