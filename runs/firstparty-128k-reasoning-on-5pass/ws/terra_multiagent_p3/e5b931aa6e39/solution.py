import sys
import math

def main():
    N = int(sys.stdin.readline())

    d = 1
    while d * d * d <= N:
        if N % d == 0:
            q = N // d
            disc = 12 * q - 3 * d * d
            if disc >= 0:
                s = math.isqrt(disc)
                if s * s == disc and s > 3 * d and (s - 3 * d) % 6 == 0:
                    y = (s - 3 * d) // 6
                    x = y + d
                    if y > 0 and x * x * x - y * y * y == N:
                        print(x, y)
                        return
        d += 1

    print(-1)

if __name__ == "__main__":
    main()