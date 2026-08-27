import sys
import math


def integer_cuberoot(n: int) -> int:
    if n < 0:
        return -1
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
    limit = integer_cuberoot(N - 1)
    isqrt = math.isqrt

    for d in range(1, limit + 1):
        if N % d != 0:
            continue

        M = N // d
        T = 4 * M - d * d

        if T < 0 or T % 3 != 0:
            continue

        S = T // 3
        s = isqrt(S)

        if s * s != S:
            continue

        if (s - d) % 2 != 0:
            continue

        y = (s - d) // 2
        if y <= 0:
            continue

        x = (s + d) // 2

        if x * x * x - y * y * y == N:
            print(x, y)
            return

    print(-1)


if __name__ == "__main__":
    main()