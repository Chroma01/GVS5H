import sys
import math

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    N = int(data[0])

    start = N % 6
    if start == 0:
        start = 6

    d = start
    while d * d * d < N:
        if N % d == 0:
            M = N // d
            T = 4 * M - d * d

            if T >= 0 and T % 3 == 0:
                u = T // 3
                r = math.isqrt(u)

                if r * r == u and (r - d) % 2 == 0 and r > d:
                    y = (r - d) // 2
                    if d * (3 * y * y + 3 * d * y + d * d) == N:
                        print(y + d, y)
                        return

        d += 6

    print(-1)

if __name__ == "__main__":
    main()