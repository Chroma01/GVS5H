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

    max_a = max(queries)
    limit = isqrt(max_a)
    if limit < 6:
        limit = 6

    # omega[n] = number of distinct prime factors of n
    omega = bytearray(limit + 1)

    for p in range(2, limit + 1):
        if omega[p] == 0:  # p is prime
            for m in range(p, limit + 1, p):
                omega[m] += 1

    # A 400 number is exactly the square of a number with exactly two
    # distinct prime factors.
    forty_numbers = [i * i for i in range(6, limit + 1) if omega[i] == 2]

    br = bisect_right
    out = []
    for a in queries:
        idx = br(forty_numbers, a) - 1
        out.append(str(forty_numbers[idx]))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()