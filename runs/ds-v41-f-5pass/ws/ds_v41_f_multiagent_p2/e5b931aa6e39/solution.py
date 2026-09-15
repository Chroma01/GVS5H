import sys
from math import isqrt


def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])

    # x^3 - y^3 = (x-y)(x^2+xy+y^2). Let d = x-y > 0, then x = y+d and
    # N = d(3y^2 + 3dy + d^2). For y >= 1 the bracket exceeds d^2, so N > d^3.
    d = 1
    while d * d * d < N:
        if N % d == 0:
            q = N // d  # q = 3y^2 + 3dy + d^2
            # Solve 3y^2 + 3dy + (d^2 - q) = 0.
            # y = (-3d + sqrt(12q - 3d^2)) / 6
            D = 12 * q - 3 * d * d
            if D >= 0:
                s = isqrt(D)
                if s * s == D:
                    num = s - 3 * d
                    if num > 0 and num % 6 == 0:
                        y = num // 6
                        if y > 0:
                            x = y + d
                            if x * x * x - y * y * y == N:
                                sys.stdout.write(f"{x} {y}\n")
                                return
        d += 1

    sys.stdout.write("-1\n")


main()