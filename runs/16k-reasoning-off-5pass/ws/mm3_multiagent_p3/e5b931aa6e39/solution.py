import sys
import math

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    # Upper bound for d: d^3 <= 4N  (from discriminant non-negative condition)
    # So d_max = floor((4N)^{1/3}) + 1 for safety
    d_max = int(round((4 * N) ** (1/3))) + 2
    # Ensure we iterate at least up to cube root of N as a fallback
    d_min_max = int(round(N ** (1/3))) + 2
    if d_max < d_min_max:
        d_max = d_min_max

    found = False
    x_res = y_res = 0
    for d in range(1, d_max + 1):
        # discriminant = 3 * d * (4*N - d**3)
        # If d**3 > 4*N, discriminant negative => stop early
        if d * d * d > 4 * N:
            break
        disc = 3 * d * (4 * N - d * d * d)
        if disc < 0:
            continue
        s = math.isqrt(disc)
        if s * s != disc:
            continue
        # y = (-3d^2 + s) / (6d)
        num = -3 * d * d + s
        if num <= 0:
            continue
        if num % (6 * d) != 0:
            continue
        y = num // (6 * d)
        if y <= 0:
            continue
        x = y + d
        # Verify (to be safe)
        if x * x * x - y * y * y == N:
            x_res, y_res = x, y
            found = True
            break

    if not found:
        print(-1)
    else:
        print(x_res, y_res)

if __name__ == "__main__":
    solve()