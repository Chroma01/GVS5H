import sys
import math

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    d = 1
    # d = x - y >= 1 must divide N, and d^3 < N is required for y >= 1
    while d * d * d < N:
        if N % d == 0:
            m = N // d
            # quadratic 3y^2 + 3dy + (d^2 - m) = 0
            # discriminant D = 9d^2 - 12(d^2 - m) = 12m - 3d^2
            D = 12 * m - 3 * d * d
            if D > 0:
                s = math.isqrt(D)
                if s * s == D:
                    num = s - 3 * d
                    if num > 0 and num % 6 == 0:
                        y = num // 6
                        x = y + d
                        if x * x * x - y * y * y == N:
                            sys.stdout.write(f"{x} {y}\n")
                            return
        d += 1
    sys.stdout.write("-1\n")

main()