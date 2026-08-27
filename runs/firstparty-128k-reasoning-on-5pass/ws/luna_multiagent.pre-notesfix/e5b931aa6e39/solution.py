import sys
import math


def main():
    n = int(sys.stdin.readline())

    # Compute floor(cuberoot(n)) exactly.
    lo, hi = 0, 1_000_001
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid * mid * mid <= n:
            lo = mid
        else:
            hi = mid
    limit = lo

    for d in range(1, limit + 1):
        if n % d != 0:
            continue

        q = n // d
        discriminant = 12 * q - 3 * d * d
        if discriminant < 0:
            continue

        s = math.isqrt(discriminant)
        if s * s != discriminant:
            continue

        numerator = s - 3 * d
        if numerator <= 0 or numerator % 6 != 0:
            continue

        y = numerator // 6
        x = y + d
        if y > 0 and x * x * x - y * y * y == n:
            print(x, y)
            return

    print(-1)


if __name__ == "__main__":
    main()