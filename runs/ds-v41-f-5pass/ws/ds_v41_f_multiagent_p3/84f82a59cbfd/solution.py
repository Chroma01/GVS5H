import sys
from math import isqrt
from bisect import bisect_right


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    q = data[0]
    queries = data[1:1 + q]

    m = isqrt(max(queries))

    # cnt[x] = number of distinct prime factors of x
    cnt = bytearray(m + 1)
    for p in range(2, m + 1):
        if cnt[p] == 0:          # p is prime
            for multiple in range(p, m + 1, p):
                cnt[multiple] += 1

    # A 400 number equals s^2 where s has exactly two distinct prime factors
    vals = [i for i in range(2, m + 1) if cnt[i] == 2]

    out = []
    for a in queries:
        limit = isqrt(a)
        idx = bisect_right(vals, limit) - 1
        s = vals[idx]
        out.append(str(s * s))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()