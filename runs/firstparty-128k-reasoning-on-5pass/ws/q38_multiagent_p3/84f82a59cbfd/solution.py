import sys
import math
from bisect import bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    q = int(data[0])
    queries = [int(x) for x in data[1:1 + q]]
    if not queries:
        return

    limit = math.isqrt(max(queries))

    # cnt[n] = number of distinct prime factors of n
    cnt = bytearray(limit + 1)
    for p in range(2, limit + 1):
        if cnt[p] == 0:  # p is prime
            for m in range(p, limit + 1, p):
                cnt[m] += 1

    # All 400 numbers are x^2 where x has exactly two distinct prime factors.
    # Iterating x increasingly keeps the squares sorted.
    values = [x * x for x in range(2, limit + 1) if cnt[x] == 2]

    out = []
    br = bisect_right
    for a in queries:
        idx = br(values, a) - 1
        if idx >= 0:
            out.append(str(values[idx]))
        else:
            out.append("0")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()