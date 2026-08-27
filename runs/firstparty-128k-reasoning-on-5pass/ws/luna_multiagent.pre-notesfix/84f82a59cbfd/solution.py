import sys
from bisect import bisect_right


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    q = data[0]
    queries = data[1:]

    limit = 1_000_000

    # Smallest-prime-factor sieve using the linear sieve method.
    spf = [0] * (limit + 1)
    primes = []

    for i in range(2, limit + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)

        for p in primes:
            v = i * p
            if v > limit:
                break
            spf[v] = p
            if p == spf[i]:
                break

    # Number of distinct prime factors for every integer.
    distinct = bytearray(limit + 1)
    candidates = []

    for x in range(2, limit + 1):
        p = spf[x]
        y = x // p
        distinct[x] = distinct[y] + (p != spf[y])

        if distinct[x] == 2:
            candidates.append(x * x)

    output = []
    for a in queries:
        output.append(str(candidates[bisect_right(candidates, a) - 1]))

    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    main()