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

    # omega[n] = number of distinct prime factors of n
    omega = bytearray(limit + 1)
    end = limit + 1

    for p in range(2, end):
        if omega[p] == 0:  # p is prime
            for m in range(p, end, p):
                omega[m] += 1

    # A 400 number is exactly x^2 where x has exactly 2 distinct prime factors.
    values = [n * n for n in range(2, end) if omega[n] == 2]

    out = []
    for a in queries:
        idx = bisect_right(values, a) - 1
        out.append(str(values[idx]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()