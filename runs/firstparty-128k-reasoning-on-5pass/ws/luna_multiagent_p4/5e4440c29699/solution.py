import sys

MOD = 998244353


def solve():
    W, H, L, R, D, U = map(int, sys.stdin.buffer.read().split())

    n = W + H + 4

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (n + 1)
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def comb(a, b):
        if b < 0 or b > a:
            return 0
        return fact[a] * invfact[b] % MOD * invfact[a - b] % MOD

    def prefix(a, b):
        """Sum of C(i+j+2, i+1), for 0 <= i <= a, 0 <= j <= b."""
        if a < 0 or b < 0:
            return 0
        return (comb(a + b + 4, a + 2) - a - b - 4) % MOD

    def paths_to(x, y):
        """Paths from every start block to (x,y), including zero-length paths."""
        if x < 0 or y < 0:
            return 0
        return (comb(x + y + 2, x + 1) - 1) % MOD

    def paths_from(x, y):
        """Paths from (x,y) to every endpoint, including the zero-length path."""
        dx = W - x
        dy = H - y
        return (comb(dx + dy + 2, dx + 1) - 1) % MOD

    # Total number of paths in the unobstructed town.
    total = (prefix(W, H) - (W + 1) * (H + 1)) % MOD

    # Sum of C((W-x)+(H-y)+2, W-x+1) over the forbidden rectangle.
    a1, a2 = W - R, W - L
    b1, b2 = H - U, H - D

    rectangle_binom_sum = (
        prefix(a2, b2)
        - prefix(a1 - 1, b2)
        - prefix(a2, b1 - 1)
        + prefix(a1 - 1, b1 - 1)
    ) % MOD

    cells = (R - L + 1) * (U - D + 1)
    invalid = (rectangle_binom_sum - cells) % MOD

    # Paths entering the forbidden rectangle from its left boundary.
    extra = 0
    if L > 0:
        for y in range(D, U + 1):
            extra = (
                extra
                + paths_to(L - 1, y) * paths_from(L, y)
            ) % MOD

    # Paths entering from its bottom boundary.
    # x=L is included: entering (L,D) from below is distinct from
    # entering it from the left, so the corner receives both corrections.
    if D > 0:
        for x in range(L, R + 1):
            extra = (
                extra
                + paths_to(x, D - 1) * paths_from(x, D)
            ) % MOD

    answer = (total - invalid - extra) % MOD
    print(answer)


if __name__ == "__main__":
    solve()