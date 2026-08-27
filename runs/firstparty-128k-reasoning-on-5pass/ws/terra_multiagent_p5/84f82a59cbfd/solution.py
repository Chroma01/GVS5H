import sys
from math import isqrt
from bisect import bisect_right

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    q = data[0]
    queries = data[1:1 + q]
    limit = isqrt(max(queries))

    omega = bytearray(limit + 1)
    for p in range(2, limit + 1):
        if omega[p] == 0:
            for multiple in range(p, limit + 1, p):
                omega[multiple] += 1

    best_root = [0] * (limit + 1)
    current = 0
    for x in range(2, limit + 1):
        if omega[x] == 2:
            current = x
        best_root[x] = current

    output = []
    for a in queries:
        root_limit = isqrt(a)
        root = best_root[root_limit]
        output.append(str(root * root))

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    main()