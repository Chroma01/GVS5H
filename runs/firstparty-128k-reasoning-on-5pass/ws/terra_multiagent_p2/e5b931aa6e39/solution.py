import sys
import math


def main():
    n = int(sys.stdin.readline())

    # Exact floor cube root of n.
    limit = 1
    while (limit + 1) ** 3 <= n:
        limit += 1

    for d in range(1, limit + 1):
        if n % d != 0:
            continue

        q = n // d

        # 3y^2 + 3dy + d^2 = q
        # Discriminant: (3d)^2 - 12(d^2 - q) = 12q - 3d^2
        disc = 12 * q - 3 * d * d
        if disc < 0:
            continue

        s = math.isqrt(disc)
        if s * s != disc:
            continue

        numerator = s - 3 * d
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