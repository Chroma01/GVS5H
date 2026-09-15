import sys
import math

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])

    d = 1
    while d * d * d <= N:
        if N % d == 0:
            Q = N // d
            # 3y^2 + 3dy + d^2 = Q  =>  y = (-3d + sqrt(12Q - 3d^2)) / 6
            Delta = 12 * Q - 3 * d * d
            if Delta >= 0:
                s = math.isqrt(Delta)
                if s * s == Delta and s > 3 * d and (s - 3 * d) % 6 == 0:
                    y = (s - 3 * d) // 6
                    x = y + d
                    if y >= 1 and x * x * x - y * y * y == N:
                        sys.stdout.write(f"{x} {y}\n")
                        return
        d += 1

    sys.stdout.write("-1\n")

main()