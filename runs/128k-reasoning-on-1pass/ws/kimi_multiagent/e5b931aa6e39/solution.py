import sys
import math

def icbrt(n: int) -> int:
    lo, hi = 0, 1
    while hi ** 3 <= n:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid ** 3 <= n:
            lo = mid
        else:
            hi = mid
    return lo

def solve() -> None:
    data = sys.stdin.read().strip()
    if not data:
        return
    N = int(data)

    # x = y + d, d > 0
    # N = d * (3y^2 + 3dy + d^2), and N > d^3, so d <= cbrt(N)
    for d in range(1, icbrt(N) + 1):
        if N % d:
            continue
        m = N // d
        if m <= d * d:
            continue
        D = 12 * m - 3 * d * d
        s = math.isqrt(D)
        if s * s != D:
            continue
        num = s - 3 * d
        if num <= 0 or num % 6:
            continue
        y = num // 6
        x = y + d
        print(x, y)
        return

    print(-1)

if __name__ == "__main__":
    solve()