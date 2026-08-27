import sys
from bisect import bisect_right
from math import isqrt


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    q = data[0]
    queries = data[1:1 + q]

    limit = isqrt(max(queries))

    spf = [0] * (limit + 1)
    primes = []

    for x in range(2, limit + 1):
        if spf[x] == 0:
            spf[x] = x
            primes.append(x)

        for p in primes:
            if p > spf[x] or p * x > limit:
                break
            spf[p * x] = p

    valid_squares = []

    for x in range(2, limit + 1):
        value = x
        distinct = 0

        while value > 1:
            p = spf[value]
            distinct += 1
            while value % p == 0:
                value //= p

            if distinct > 2:
                break

        if distinct == 2:
            valid_squares.append(x * x)

    output = []
    for a in queries:
        output.append(str(valid_squares[bisect_right(valid_squares, a) - 1]))

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    main()