import sys

MOD = 998244353

def main():
    W, H, L, R, D, U = map(int, sys.stdin.readline().split())

    nmax = W + H + 4
    fact = [1] * (nmax + 1)
    for i in range(1, nmax + 1):
        fact[i] = fact[i - 1] * i % MOD

    ifact = [1] * (nmax + 1)
    ifact[nmax] = pow(fact[nmax], MOD - 2, MOD)
    for i in range(nmax, 0, -1):
        ifact[i - 1] = ifact[i] * i % MOD

    def comb(n, k):
        if k < 0 or k > n:
            return 0
        return fact[n] * ifact[k] % MOD * ifact[n - k] % MOD

    # Sum over 0 <= i <= a, 0 <= j <= b of C(i+j+2, i+1).
    def prefix_c(a, b):
        if a < 0 or b < 0:
            return 0
        return (comb(a + b + 4, a + 2) - (a + 1) - (b + 3)) % MOD

    # Number of paths from arbitrary start in [0,a] x [0,b]
    # to (a,b), equivalently from (0,0) to arbitrary endpoint.
    def all_to_corner(a, b):
        return (comb(a + b + 2, a + 1) - 1) % MOD

    # All monotone paths in the complete (W+1) by (H+1) grid.
    total = (prefix_c(W, H) - (W + 1) * (H + 1)) % MOD

    # Paths whose starting point is in the removed rectangle.
    ix0, ix1 = W - R, W - L
    iy0, iy1 = H - U, H - D
    starts_hole = (
        prefix_c(ix1, iy1)
        - prefix_c(ix0 - 1, iy1)
        - prefix_c(ix1, iy0 - 1)
        + prefix_c(ix0 - 1, iy0 - 1)
        - (R - L + 1) * (U - D + 1)
    ) % MOD

    # Paths starting outside which first enter the hole from its left side.
    enter_left = 0
    if L > 0:
        for y in range(D, U + 1):
            enter_left += all_to_corner(L - 1, y) * all_to_corner(W - L, H - y)
        enter_left %= MOD

    # Paths starting outside which first enter the hole from its bottom side.
    enter_bottom = 0
    if D > 0:
        for x in range(L, R + 1):
            enter_bottom += all_to_corner(x, D - 1) * all_to_corner(W - x, H - D)
        enter_bottom %= MOD

    ans = (total - starts_hole - enter_left - enter_bottom) % MOD
    print(ans)

if __name__ == "__main__":
    main()