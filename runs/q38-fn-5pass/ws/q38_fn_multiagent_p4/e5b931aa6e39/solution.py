import sys
import math


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])

    # Find the largest d such that d^3 < N.
    # Since y >= 1, x^3 - y^3 > (x-y)^3, so d = x-y must satisfy d^3 < N.
    hi = 1
    while hi * hi * hi < N:
        hi *= 2

    lo = 0
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid * mid * mid < N:
            lo = mid
        else:
            hi = mid

    limit = lo
    isqrt = math.isqrt

    for d in range(1, limit + 1):
        if N % d != 0:
            continue

        m = N // d

        # Solve 3*y^2 + 3*d*y + d^2 = m.
        # Discriminant D = (3*d)^2 - 4*3*(d^2 - m) = 12*m - 3*d^2.
        D = 12 * m - 3 * d * d
        if D < 0:
            continue

        s = isqrt(D)
        if s * s != D:
            continue

        # y = (-3*d + s) / 6
        num = s - 3 * d
        if num <= 0 or num % 6 != 0:
            continue

        y = num // 6
        if y <= 0:
            continue

        x = y + d

        # Final verification (optional, but safe).
        if x * x * x - y * y * y == N:
            print(x, y)
            return

    print(-1)


if __name__ == "__main__":
    main()