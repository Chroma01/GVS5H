import sys
from array import array

MOD = 998244353


def solve():
    W, H, L, R, D, U = map(int, sys.stdin.buffer.readline().split())

    nmax = W + H + 4

    fact = array('I', [1]) * (nmax + 1)
    for i in range(1, nmax + 1):
        fact[i] = (fact[i - 1] * i) % MOD

    invfact = array('I', [1]) * (nmax + 1)
    invfact[nmax] = pow(fact[nmax], MOD - 2, MOD)
    for i in range(nmax, 0, -1):
        invfact[i - 1] = (invfact[i] * i) % MOD

    def comb(n, k):
        if k < 0 or k > n:
            return 0
        return (fact[n] * invfact[k] % MOD) * invfact[n - k] % MOD

    # Number of all monotone paths starting at one fixed corner of
    # an a by b rectangle, allowing arbitrary endpoint.
    def paths_from_corner(a, b):
        return (comb(a + b + 2, a + 1) - 1) % MOD

    # Sum_{0 <= i <= a, 0 <= j <= b} C(i+j+2, i+1).
    # It is zero if the rectangle is empty.
    def binom_prefix(a, b):
        if a < 0 or b < 0:
            return 0
        return (comb(a + b + 4, a + 2) - a - b - 4) % MOD

    # Full grid total.
    full_total = (
        binom_prefix(W, H) - (W + 1) * (H + 1)
    ) % MOD

    # Paths whose starting point is inside the forbidden rectangle.
    # For each such start, all suffixes are unrestricted in the full grid.
    x_lo = W - R
    x_hi = W - L
    y_lo = H - U
    y_hi = H - D

    raw_suffix_sum = (
        binom_prefix(x_hi, y_hi)
        - binom_prefix(x_lo - 1, y_hi)
        - binom_prefix(x_hi, y_lo - 1)
        + binom_prefix(x_lo - 1, y_lo - 1)
    ) % MOD

    hole_cells = (R - L + 1) * (U - D + 1)
    bad = (raw_suffix_sum - hole_cells) % MOD

    # Paths starting outside and first entering through the left boundary.
    if L > 0:
        left_entries = 0
        for y in range(D, U + 1):
            prefix = paths_from_corner(L - 1, y)
            suffix = paths_from_corner(W - L, H - y)
            left_entries += prefix * suffix
        bad = (bad + left_entries) % MOD

    # Paths starting outside and first entering through the bottom boundary.
    if D > 0:
        bottom_entries = 0
        for x in range(L, R + 1):
            prefix = paths_from_corner(x, D - 1)
            suffix = paths_from_corner(W - x, H - D)
            bottom_entries += prefix * suffix
        bad = (bad + bottom_entries) % MOD

    print((full_total - bad) % MOD)


if __name__ == "__main__":
    solve()