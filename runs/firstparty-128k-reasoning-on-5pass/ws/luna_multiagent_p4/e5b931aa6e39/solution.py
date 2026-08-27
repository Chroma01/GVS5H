import sys
import math


def integer_cuberoot(n: int) -> int:
    r = int(n ** (1.0 / 3.0))
    while (r + 1) ** 3 <= n:
        r += 1
    while r ** 3 > n:
        r -= 1
    return r


def solve() -> None:
    n = int(sys.stdin.readline())
    limit = integer_cuberoot(n)

    for d in range(1, limit + 1):
        if n % d != 0:
            continue

        m = n // d
        discriminant = 12 * m - 3 * d * d
        if discriminant < 0:
            continue

        root = math.isqrt(discriminant)
        if root * root != discriminant:
            continue

        numerator = root - 3 * d
        if numerator <= 0 or numerator % 6 != 0:
            continue

        y = numerator // 6
        x = y + d

        if y > 0 and x ** 3 - y ** 3 == n:
            print(x, y)
            return

    print(-1)


if __name__ == "__main__":
    solve()