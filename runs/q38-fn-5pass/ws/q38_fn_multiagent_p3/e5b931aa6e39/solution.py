import sys
from math import isqrt

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])

    d = 1
    while True:
        d2 = d * d
        if d2 * d >= N:
            break

        if N % d == 0:
            m = N // d
            disc = 12 * m - 3 * d2
            s = isqrt(disc)

            if s * s == disc:
                num = s - 3 * d
                if num > 0 and num % 6 == 0:
                    y = num // 6
                    if d * (3 * y * y + 3 * d * y + d2) == N:
                        print(y + d, y)
                        return

        d += 1

    print(-1)

if __name__ == "__main__":
    solve()