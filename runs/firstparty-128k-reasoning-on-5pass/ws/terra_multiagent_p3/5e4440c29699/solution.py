import sys

MOD = 998244353

def solve():
    W, H, L, R, D, U = map(int, sys.stdin.buffer.readline().split())

    nmax = W + H + 3
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

    # Total monotone paths in the complete (W+1) by (H+1) grid.
    # For fixed horizontal displacement a, summing over all vertical
    # displacements and all possible starts gives C(a+H+2, a+2).
    total = 0
    for a in range(W + 1):
        total += (W + 1 - a) * comb(a + H + 2, a + 2)
    total %= MOD

    def prefix(x, y):
        # Number of paths from any full-grid start to (x,y).
        return (comb(x + y + 2, x + 1) - 1) % MOD

    def suffix(x, y):
        # Number of paths from (x,y) to any full-grid end.
        a = W - x
        b = H - y
        return (comb(a + b + 2, a + 1) - 1) % MOD

    invalid = 0

    # Paths whose first forbidden vertex is entered from the left.
    if L > 0:
        for y in range(D, U + 1):
            invalid += prefix(L - 1, y) * suffix(L, y)
        invalid %= MOD

    # Paths whose first forbidden vertex is entered from below.
    if D > 0:
        for x in range(L, R + 1):
            invalid += prefix(x, D - 1) * suffix(x, D)
        invalid %= MOD

    # Invalid paths starting inside the removed rectangle.
    # Write a=W-x and b=H-y. For each fixed a, hockey-stick gives:
    # sum_b C(a+b+2, a+1)
    # = C(a+B1+3,a+2)-C(a+B0+2,a+2).
    A0 = W - R
    A1 = W - L
    B0 = H - U
    B1 = H - D

    start_inside = 0
    for a in range(A0, A1 + 1):
        start_inside += comb(a + B1 + 3, a + 2)
        start_inside -= comb(a + B0 + 2, a + 2)

    hole_size = (R - L + 1) * (U - D + 1)
    start_inside -= hole_size
    invalid = (invalid + start_inside) % MOD

    print((total - invalid) % MOD)

if __name__ == "__main__":
    solve()