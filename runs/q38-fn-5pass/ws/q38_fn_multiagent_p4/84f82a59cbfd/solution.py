import sys
import math
import bisect


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    q = int(data[0])
    queries = [int(x) for x in data[1:1 + q]]
    if not queries:
        return

    max_a = max(queries)
    limit = math.isqrt(max_a)

    # omega[n] = number of distinct prime factors of n
    omega = [0] * (limit + 1)

    for i in range(2, limit + 1):
        if omega[i] == 0:  # i is prime
            for j in range(i, limit + 1, i):
                omega[j] += 1

    # A 400 number is exactly x^2 where x has exactly two distinct prime factors.
    values = [i * i for i in range(2, limit + 1) if omega[i] == 2]

    out = []
    bisect_right = bisect.bisect_right

    for a in queries:
        idx = bisect_right(values, a) - 1
        out.append(str(values[idx]))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()