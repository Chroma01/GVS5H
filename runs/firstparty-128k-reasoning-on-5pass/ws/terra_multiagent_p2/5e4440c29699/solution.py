import sys

MOD = 998244353

def solve():
    W, H, L, R, D, U = map(int, sys.stdin.buffer.read().split())

    nmax = W + H + 4
    fact = [1] * (nmax + 1)
    for i in range(1, nmax + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (nmax + 1)
    invfact[nmax] = pow(fact[nmax], MOD - 2, MOD)
    for i in range(nmax, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def comb(n, k):
        if k < 0 or k > n:
            return 0
        return fact[n] * invfact[k] % MOD * invfact[n - k] % MOD

    # Number of all directed paths in the complete (W+1) by (H+1) grid.
    total = (
        comb(W + H + 4, W + 2)
        - W - H - 4
        - (W + 1) * (H + 1)
    ) % MOD

    # Full-grid count of paths ending at (x, y), over all possible starts.
    def ending_count(x, y):
        return (comb(x + y + 2, x + 1) - 1) % MOD

    # Full-grid count of paths starting at (x, y), over all possible ends.
    def starting_count(x, y):
        dx = W - x
        dy = H - y
        return (comb(dx + dy + 2, dx + 1) - 1) % MOD

    # Sum_{0<=i<=b, 0<=j<=d} C(i+j, i).
    def prefix_binom_sum(b, d):
        if b < 0 or d < 0:
            return 0
        return (comb(b + d + 2, b + 1) - 1) % MOD

    # Sum of suffix counts starting from every point of the removed rectangle.
    # With i=W-x+1 and j=H-y+1, each binomial term is C(i+j, i).
    il, ir = W - R + 1, W - L + 1
    jl, jr = H - U + 1, H - D + 1
    hole_binom_sum = (
        prefix_binom_sum(ir, jr)
        - prefix_binom_sum(il - 1, jr)
        - prefix_binom_sum(ir, jl - 1)
        + prefix_binom_sum(il - 1, jl - 1)
    ) % MOD
    hole_area = (R - L + 1) * (U - D + 1)
    invalid = (hole_binom_sum - hole_area) % MOD

    # First entry through the left side of the hole.
    if L > 0:
        for y in range(D, U + 1):
            invalid += ending_count(L - 1, y) * starting_count(L, y)
            invalid %= MOD

    # First entry through the bottom side of the hole.
    if D > 0:
        for x in range(L, R + 1):
            invalid += ending_count(x, D - 1) * starting_count(x, D)
            invalid %= MOD

    print((total - invalid) % MOD)

if __name__ == "__main__":
    solve()