import sys
import math
import bisect

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if len(data) <= 1:
        return

    queries = data[1:]
    max_a = max(queries)

    # Any valid 400 number is m^2, where m has exactly two distinct prime factors.
    # Since A <= 10^12, m <= isqrt(A) <= 10^6.
    limit = math.isqrt(max_a)

    # distinct[m] = number of distinct prime factors of m
    distinct = [0] * (limit + 1)

    # Sieve primes up to limit
    is_prime = bytearray(b'\x01') * (limit + 1)
    if limit >= 0:
        is_prime[0] = 0
    if limit >= 1:
        is_prime[1] = 0

    for i in range(2, math.isqrt(limit) + 1):
        if is_prime[i]:
            start = i * i
            is_prime[start:limit + 1:i] = b'\x00' * (((limit - start) // i) + 1)

    primes = [i for i in range(2, limit + 1) if is_prime[i]]

    # Count each distinct prime once per multiple, not once per exponent.
    for p in primes:
        for m in range(p, limit + 1, p):
            distinct[m] += 1

    # Valid bases m >= 6, then form valid 400 numbers as m^2.
    valid_squares = [m * m for m in range(6, limit + 1) if distinct[m] == 2]

    out = []
    for a in queries:
        idx = bisect.bisect_right(valid_squares, a) - 1
        out.append(str(valid_squares[idx]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()