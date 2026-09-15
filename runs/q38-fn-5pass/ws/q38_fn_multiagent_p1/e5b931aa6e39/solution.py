import sys
import math


def icbrt(n: int) -> int:
    """Return floor(cuberoot(n)) using exact integer arithmetic."""
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


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    limit = icbrt(N)
    isqrt = math.isqrt

    for d in range(1, limit + 1):
        if N % d != 0:
            continue

        m = N // d

        # Need 3y^2 + 3dy + d^2 = m.
        # Completing the square:
        #   3(2y + d)^2 = 4m - d^2
        val = 4 * m - d * d
        if val % 3 != 0:
            continue

        u2 = val // 3
        u = isqrt(u2)
        if u * u != u2:
            continue

        # u = 2y + d, so y = (u - d) / 2 must be a positive integer.
        if u > d and ((u - d) & 1) == 0:
            y = (u - d) // 2
            x = y + d
            print(x, y)
            return

    print(-1)


if __name__ == "__main__":
    main()