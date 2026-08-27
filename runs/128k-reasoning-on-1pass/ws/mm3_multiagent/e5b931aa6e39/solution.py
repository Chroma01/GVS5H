import sys
import math

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])

    d = 1
    # only d = x - y with d^3 ≤ N can appear
    while d * d * d <= N:
        if N % d == 0:
            M = N // d                     # M = x^2 + x*y + y^2
            # discriminant of the quadratic 3y^2 + 3d y + d^2 = M
            delta = 12 * M - 3 * d * d
            if delta >= 0:
                s = math.isqrt(delta)
                if s * s == delta:
                    num = s - 3 * d         # numerator of y
                    if num > 0 and num % 6 == 0:
                        y = num // 6
                        x = y + d
                        if x**3 - y**3 == N:
                            print(x, y)
                            return
        d += 1

    print(-1)

if __name__ == "__main__":
    solve()