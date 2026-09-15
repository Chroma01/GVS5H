import sys
from math import isqrt
from bisect import bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    q = int(data[0])
    queries = [int(x) for x in data[1:1 + q]]

    max_a = max(queries)
    n = isqrt(max_a)  # largest possible base; at most 10^6

    # omega[m] = number of distinct prime factors of m
    omega = bytearray(n + 1)
    comp = bytearray(n + 1)  # composite flags for the prime sieve

    for i in range(2, n + 1):
        if not comp[i]:
            # every multiple of the prime i gets one more distinct factor
            for j in range(i, n + 1, i):
                omega[j] += 1
            ii = i * i
            if ii <= n:
                for j in range(ii, n + 1, i):
                    comp[j] = 1

    # 400 numbers are exactly m^2 for m with exactly two distinct primes
    vals = [m * m for m in range(2, n + 1) if omega[m] == 2]
    # vals is already strictly increasing because m increases

    out = []
    br = bisect_right
    for a in queries:
        out.append(vals[br(vals, a) - 1])

    sys.stdout.write("\n".join(map(str, out)) + "\n")


if __name__ == "__main__":
    main()