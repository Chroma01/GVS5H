import sys
from bisect import bisect_right
from math import isqrt

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    q = data[0]
    queries = data[1:]

    limit = isqrt(max(queries))

    omega = bytearray(limit + 1)
    for p in range(2, limit + 1):
        if omega[p] == 0:
            for multiple in range(p, limit + 1, p):
                omega[multiple] += 1

    values = [x * x for x in range(2, limit + 1) if omega[x] == 2]

    out = []
    for a in queries:
        out.append(str(values[bisect_right(values, a) - 1]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()