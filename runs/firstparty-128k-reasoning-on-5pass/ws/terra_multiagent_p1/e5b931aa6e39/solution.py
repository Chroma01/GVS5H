import sys
import math


def integer_cuberoot(n: int) -> int:
    lo, hi = 0, 1
    while hi * hi * hi <= n:
        hi *= 2

    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid * mid * mid <= n:
            lo = mid
        else:
            hi = mid
    return lo


def main() -> None:
    n = int(sys.stdin.readline())
    limit = integer_cuberoot(n)

    for d in range(1, limit + 1):
        if n % d != 0:
            continue

        q = n // d
        # 3y^2 + 3dy + d^2 = q
        # Discriminant: D = 12q - 3d^2
        disc = 12 * q - 3 * d * d
        if disc < 0:
            continue

        root = math.isqrt(disc)
        if root * root != disc:
            continue

        numerator = root - 3 * d
        if numerator <= 0 or numerator % 6 != 0:
            continue

        y = numerator // 6
        x = y + d

        if x > 0 and y > 0 and x * x * x - y * y * y == n:
            print(x, y)
            return

    print(-1)


if __name__ == "__main__":
    main()