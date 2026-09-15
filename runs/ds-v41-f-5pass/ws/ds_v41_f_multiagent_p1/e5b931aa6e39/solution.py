import sys
from math import isqrt

def main():
    data = sys.stdin.readline().strip()
    if not data:
        data = sys.stdin.read().strip()
    N = int(data)

    def icbrt(n):
        if n < 0:
            raise ValueError
        c = round(n ** (1.0 / 3.0))
        c = int(c)
        if c < 0:
            c = 0
        # correct with integer arithmetic
        while (c + 1) ** 3 <= n:
            c += 1
        while c > 0 and c ** 3 > n:
            c -= 1
        return c

    L = icbrt(N)
    for d in range(1, L + 1):
        if N % d != 0:
            continue
        M = N // d
        D = 12 * M - 3 * d * d
        if D < 0:
            continue
        s = isqrt(D)
        if s * s != D:
            continue
        if (-3 * d + s) % 6 != 0:
            continue
        y = (-3 * d + s) // 6
        if y <= 0:
            continue
        if d * (3 * y * y + 3 * d * y + d * d) == N:
            x = y + d
            print(x, y)
            return
    print(-1)

main()