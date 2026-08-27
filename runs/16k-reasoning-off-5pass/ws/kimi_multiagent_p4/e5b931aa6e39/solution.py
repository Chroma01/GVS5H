import sys
import math

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])

    # Integer cube root of N (exact, no float issues)
    c = int(round(N ** (1.0 / 3.0))) + 2
    while c ** 3 > N:
        c -= 1
    while (c + 1) ** 3 <= N:
        c += 1
    # d = x - y satisfies d^3 < N, so d <= c suffices (c^3 <= N)

    for d in range(1, c + 1):
        if N % d != 0:
            continue
        m = N // d  # m = 3y^2 + 3dy + d^2
        # Discriminant of 3y^2 + 3dy + (d^2 - m) = 0
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
        if y >= 1 and x * x * x - y * y * y == N:
            print(x, y)
            return
    print(-1)

main()