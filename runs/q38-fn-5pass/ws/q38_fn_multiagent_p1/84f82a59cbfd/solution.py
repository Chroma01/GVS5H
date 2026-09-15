import sys
from math import isqrt
from bisect import bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    q = int(data[0])
    queries = [int(x) for x in data[1:1 + q]]
    if not queries:
        return

    limit = isqrt(max(queries))

    # omega[n] = number of distinct prime factors of n
    omega = bytearray(limit + 1)

    # Sieve: for every prime p, add 1 to all multiples of p.
    # A number i is prime iff omega[i] is still 0 before processing it.
    for i in range(2, limit + 1):
        if omega[i] == 0:
            for j in range(i, limit + 1, i):
                omega[j] += 1

    # A 400 number is exactly the square of a number with exactly
    # two distinct prime factors.
    valid_squares = [
        i * i
        for i in range(2, limit + 1)
        if omega[i] == 2
    ]

    out = []
    br = bisect_right

    for a in queries:
        r = isqrt(a)
        # Any square <= a has base <= r, so its square is <= r*r.
        idx = br(valid_squares, r * r) - 1
        if idx >= 0:
            out.append(str(valid_squares[idx]))
        else:
            out.append("0")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()