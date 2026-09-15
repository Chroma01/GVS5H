import sys
import math


def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])

    d = 1
    while d * d * d <= N:
        if N % d == 0:
            Q = N // d
            # 3y^2 + 3dy + d^2 = Q  =>  discriminant = 12Q - 3d^2
            disc = 12 * Q - 3 * d * d
            if disc >= 0:
                r = math.isqrt(disc)
                if r * r == disc:
                    num = r - 3 * d           # must equal 6y
                    if num > 0 and num % 6 == 0:
                        y = num // 6
                        x = y + d
                        sys.stdout.write(f"{x} {y}\n")
                        return
        d += 1

    sys.stdout.write("-1\n")


main()