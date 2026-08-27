import sys
import math
from bisect import bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    # First token is Q; the remaining tokens are the queries.
    queries = [int(x) for x in data[1:]]
    if not queries:
        return

    max_a = max(queries)
    r = math.isqrt(max_a)

    # cnt[i] = number of distinct prime factors of i
    cnt = bytearray(r + 1)
    limit = r + 1

    for i in range(2, limit):
        if cnt[i] == 0:  # i is prime
            for j in range(i, limit, i):
                cnt[j] += 1

    # A 400 number is exactly the square of an integer with 2 distinct prime factors.
    values = [i * i for i in range(2, limit) if cnt[i] == 2]

    out = []
    br = bisect_right
    for a in queries:
        idx = br(values, a) - 1
        out.append(str(values[idx]))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()