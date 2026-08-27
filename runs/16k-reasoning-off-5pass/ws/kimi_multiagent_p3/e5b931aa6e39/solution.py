import sys
import math

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])

    # Integer cube root of N (largest r with r^3 <= N)
    r = int(round(N ** (1.0 / 3.0)))
    if r < 1:
        r = 1
    while (r + 1) ** 3 <= N:
        r += 1
    while r ** 3 > N:
        r -= 1

    # N = (x - y) * (x^2 + xy + y^2)
    # Let d = x - y >= 1, then x^2 + xy + y^2 = 3y^2 + 3dy + d^2.
    # Since 3y^2 + 3dy + d^2 > d^2, we have d^3 < N, so d <= cbrt(N).
    for d in range(1, r + 1):
        if N % d != 0:
            continue
        m = N // d
        # Solve 3y^2 + 3dy + d^2 = m
        # y = (-3d + sqrt(12m - 3d^2)) / 6
        D = 12 * m - 3 * d * d
        if D < 0:
            continue
        s = math.isqrt(D)
        if s * s != D:
            continue
        num = s - 3 * d
        if num <= 0 or num % 6 != 0:
            continue
        y = num // 6
        x = y + d
        # Verify (cheap safety check)
        if x * x * x - y * y * y == N:
            sys.stdout.write(f"{x} {y}\n")
            return

    sys.stdout.write("-1\n")

main()