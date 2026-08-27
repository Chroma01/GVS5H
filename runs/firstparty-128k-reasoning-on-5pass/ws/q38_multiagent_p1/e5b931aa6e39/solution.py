import sys
import math


def floor_cuberoot(n):
    lo, hi = 0, 1
    while hi * hi * hi <= n:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid * mid * mid <= n:
            lo = mid
        else:
            hi = mid
    return lo


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    L = floor_cuberoot(N)
    isqrt = math.isqrt

    for d in range(1, L + 1):
        if N % d != 0:
            continue

        q = N // d
        d2 = d * d
        D = 12 * q - 3 * d2

        if D < 0:
            continue

        s = isqrt(D)
        if s * s != D:
            continue

        t = s - 3 * d
        if t > 0 and t % 6 == 0:
            y = t // 6
            x = y + d
            print(x, y)
            return

    print(-1)


if __name__ == "__main__":
    main()