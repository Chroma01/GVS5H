import sys
import math

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    d = 1
    while d * d * d < N:
        if N % d == 0:
            m = N // d
            D = 12 * m - 3 * d * d
            if D >= 0:
                r = math.isqrt(D)
                if r * r == D:
                    num = r - 3 * d
                    if num > 0 and num % 6 == 0:
                        y = num // 6
                        if y >= 1:
                            x = y + d
                            if x * x * x - y * y * y == N:
                                sys.stdout.write(f"{x} {y}\n")
                                return
        d += 1
    sys.stdout.write("-1\n")

main()