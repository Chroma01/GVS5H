import sys
import math


def integer_cuberoot(n: int) -> int:
    lo = 0
    hi = 1
    while hi * hi * hi <= n:
        hi *= 2

    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid * mid * mid <= n:
            lo = mid
        else:
            hi = mid

    return lo


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    limit = integer_cuberoot(N)
    isqrt = math.isqrt

    for d in range(1, limit + 1):
        if N % d != 0:
            continue

        m = N // d

        # With x = y + d:
        # N = d * (3*y^2 + 3*d*y + d^2)
        # So 3*y^2 + 3*d*y + (d^2 - m) = 0.
        # Discriminant = (3*d)^2 - 4*3*(d^2 - m) = 12*m - 3*d*d.
        disc = 12 * m - 3 * d * d
        if disc < 0:
            continue

        s = isqrt(disc)
        if s * s != disc:
            continue

        # y = (-3*d + s) / 6
        num = s - 3 * d
        if num <= 0 or num % 6 != 0:
            continue

        y = num // 6
        x = y + d

        # Final safety check; also guarantees y > 0 and x > 0.
        if x > 0 and y > 0 and x * x * x - y * y * y == N:
            print(x, y)
            return

    print(-1)


if __name__ == "__main__":
    main()