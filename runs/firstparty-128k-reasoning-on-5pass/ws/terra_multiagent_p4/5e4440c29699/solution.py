import sys
from array import array

MOD = 998244353

def main():
    W, H, L, R, D, U = map(int, sys.stdin.buffer.readline().split())

    nmax = W + H + 4

    fact = array('I', [0]) * (nmax + 1)
    ifact = array('I', [0]) * (nmax + 1)

    fact[0] = 1
    for i in range(1, nmax + 1):
        fact[i] = (fact[i - 1] * i) % MOD

    ifact[nmax] = pow(fact[nmax], MOD - 2, MOD)
    for i in range(nmax, 0, -1):
        ifact[i - 1] = (ifact[i] * i) % MOD

    def comb(n, k):
        if k < 0 or k > n:
            return 0
        return (fact[n] * ifact[k] % MOD) * ifact[n - k] % MOD

    # Sum_{0<=x<=a, 0<=y<=b} C(x+y+2, x+1).
    def prefix_sum(a, b):
        if a < 0 or b < 0:
            return 0
        return (comb(a + b + 4, a + 2) - a - b - 4) % MOD

    # Total paths in a full W x H lattice rectangle.
    total = (prefix_sum(W, H) - (W + 1) * (H + 1)) % MOD

    # For a forbidden vertex (x,y), the number of unrestricted suffixes
    # beginning there and ending anywhere in the outer grid.
    def suffix(x, y):
        return (comb(W - x + H - y + 2, W - x + 1) - 1) % MOD

    # Every forbidden vertex can be the first forbidden vertex by starting there.
    # Sum suffixes over the forbidden rectangle.
    a0, a1 = W - R, W - L
    b0, b1 = H - U, H - D
    rectangle_k_sum = (
        prefix_sum(a1, b1)
        - prefix_sum(a0 - 1, b1)
        - prefix_sum(a1, b0 - 1)
        + prefix_sum(a0 - 1, b0 - 1)
    ) % MOD
    bad = (rectangle_k_sum - (R - L + 1) * (U - D + 1)) % MOD

    # Extra ways for the first forbidden vertex to be entered from below.
    if D > 0:
        for x in range(L, R + 1):
            # Number of unrestricted prefixes ending at (x, D-1).
            pref = (comb(x + D + 1, x + 1) - 1) % MOD
            bad = (bad + pref * suffix(x, D)) % MOD

    # Extra ways for the first forbidden vertex to be entered from the left.
    if L > 0:
        for y in range(D, U + 1):
            # Number of unrestricted prefixes ending at (L-1, y).
            pref = (comb(L + y + 1, L) - 1) % MOD
            bad = (bad + pref * suffix(L, y)) % MOD

    print((total - bad) % MOD)

if __name__ == "__main__":
    main()