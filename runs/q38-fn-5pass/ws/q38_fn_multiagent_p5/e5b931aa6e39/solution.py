import sys
from math import isqrt

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])

    # Largest d such that d^3 < N.
    # Since N <= 10^18, d <= 999999.
    lo, hi = 0, 10**6 + 1
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid * mid * mid < N:
            lo = mid
        else:
            hi = mid

    for d in range(1, lo + 1):
        if N % d != 0:
            continue

        M = N // d

        # 3y^2 + 3dy + d^2 = M
        # Discriminant: D = 12M - 3d^2
        D = 12 * M - 3 * d * d
        if D < 0:
            continue

        s = isqrt(D)
        if s * s != D:
            continue

        num = s - 3 * d
        if num <= 0 or num % 6 != 0:
            continue

        y = num // 6
        x = y + d

        if x > 0 and y > 0 and x * x * x - y * y * y == N:
            print(x, y)
            return

    print(-1)

if __name__ == "__main__":
    solve()