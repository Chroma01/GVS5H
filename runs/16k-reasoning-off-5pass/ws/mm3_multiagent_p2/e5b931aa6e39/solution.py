import sys
import math

def solve():
    data = sys.stdin.read().strip()
    if not data:
        return
    N = int(data)
    # Upper bound for d = x - y. Since x >= y+1, we have N = d*(3y^2+3dy+d^2) >= d*d^2 = d^3.
    # So d^3 <= N, hence d <= floor(N**(1/3)) + 1.
    max_d = int(round(N ** (1/3))) + 2
    # Ensure we don't iterate excessively if N is huge but exact cube root is small
    # but the +2 is safe.
    for d in range(1, max_d):
        # d^3 might exceed N, but we can still check; if d^3 > N, then 12dN - 3d^4 becomes negative.
        # discriminant = 12*d*N - 3*d^4
        disc = 12 * d * N - 3 * d * d * d * d
        if disc < 0:
            # As d increases, disc becomes more negative. We can break.
            # But careful: disc might dip below 0 then come back? No, for fixed N, disc = 3d(4N - d^3).
            # It increases while d^3 < 4N, then decreases. But if d^3 > N, we have no solution because d^3 <= N is necessary?
            # Actually d^3 <= N is necessary? Let's check: N = d * (3y^2+3dy+d^2) >= d * d^2 = d^3. So yes, d^3 <= N is necessary.
            # So we can break when d^3 > N.
            if d * d * d > N:
                break
            continue
        # Compute integer square root of disc
        s = math.isqrt(disc)
        if s * s != disc:
            continue
        # y = (-3d^2 + s) / (6d)
        num = -3 * d * d + s
        den = 6 * d
        # y must be positive integer
        if num <= 0:
            continue
        if num % den != 0:
            continue
        y = num // den
        x = y + d
        if x <= 0 or y <= 0:
            continue
        # Verify
        if x**3 - y**3 == N:
            print(f"{x} {y}")
            return
    print("-1")

if __name__ == "__main__":
    solve()