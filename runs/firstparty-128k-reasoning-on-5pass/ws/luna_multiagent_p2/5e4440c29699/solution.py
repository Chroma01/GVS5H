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

    # Number of monotone paths from any point southwest of (x, y) to (x, y).
    def F(x, y):
        if x < 0 or y < 0:
            return 0
        return (comb(x + y + 2, x + 1) - 1) % MOD

    # Two-dimensional prefix sum of F:
    # G(x,y) = sum_{a=0..x} sum_{b=0..y} F(a,b).
    def G(x, y):
        if x < 0 or y < 0:
            return 0
        return (
            comb(x + y + 4, x + 2)
            - x - y - 4
            - (x + 1) * (y + 1)
        ) % MOD

    def rect_sum_f(x1, x2, y1, y2):
        if x1 > x2 or y1 > y2:
            return 0
        return (
            G(x2, y2)
            - G(x1 - 1, y2)
            - G(x2, y1 - 1)
            + G(x1 - 1, y1 - 1)
        ) % MOD

    # All unrestricted paths, including paths of length zero.
    total = G(W, H)

    # Paths whose starting block lies inside the forbidden rectangle.
    inside = rect_sum_f(W - R, W - L, H - U, H - D)
    invalid = inside

    # First entry through the left side of the forbidden rectangle.
    if L > 0:
        for y in range(D, U + 1):
            prefix = F(L - 1, y)
            suffix = F(W - L, H - y)
            invalid = (invalid + prefix * suffix) % MOD

    # First entry through the bottom side of the forbidden rectangle.
    if D > 0:
        for x in range(L, R + 1):
            prefix = F(x, D - 1)
            suffix = F(W - x, H - D)
            invalid = (invalid + prefix * suffix) % MOD

    print((total - invalid) % MOD)


if __name__ == "__main__":
    solve()