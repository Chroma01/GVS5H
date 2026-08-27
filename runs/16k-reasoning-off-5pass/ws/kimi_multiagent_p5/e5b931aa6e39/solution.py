import sys
import math

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])

    # d = x - y >= 1, and N = d * (x^2 + xy + y^2) > d^3, so d <= cube_root(N) <= 10^6
    # Integer cube root via round(N ** (1/3)) then adjust (safe: result <= ~10^6)
    r = int(round(N ** (1.0 / 3.0)))
    while r * r * r > N:
        r -= 1
    while (r + 1) * (r + 1) * (r + 1) <= N:
        r += 1
    cbrt = r

    for d in range(1, cbrt + 1):
        if N % d != 0:
            continue
        m = N // d  # m = x^2 + xy + y^2 = 3y^2 + 3dy + d^2
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
            sys.stdout.write(f"{x} {y}\n")
            return

    sys.stdout.write("-1\n")

main()