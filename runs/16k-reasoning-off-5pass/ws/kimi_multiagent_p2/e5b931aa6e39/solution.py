import sys
import math

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])

    # Integer cube root of N (largest r with r^3 <= N)
    r = int(round(N ** (1.0 / 3.0)))
    while (r + 1) ** 3 <= N:
        r += 1
    while r ** 3 > N:
        r -= 1

    out = None
    for d in range(1, r + 1):
        if N % d != 0:
            continue
        m = N // d
        # Need 3y^2 + 3dy + d^2 = m
        # Discriminant: 9d^2 - 12(d^2 - m) = 12m - 3d^2
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
        if x * x * x - y * y * y == N:
            out = (x, y)
            break

    if out is None:
        sys.stdout.write("-1\n")
    else:
        sys.stdout.write(f"{out[0]} {out[1]}\n")

main()