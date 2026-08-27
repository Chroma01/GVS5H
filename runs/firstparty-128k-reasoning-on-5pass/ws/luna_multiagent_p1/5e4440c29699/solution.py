import sys

MOD = 998244353


def solve():
    W, H, L, R, D, U = map(int, sys.stdin.readline().split())

    n = W + H + 6
    fact = [1] * n
    for i in range(1, n):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * n
    invfact[-1] = pow(fact[-1], MOD - 2, MOD)
    for i in range(n - 1, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def comb(a, b):
        if a < 0 or b < 0 or b > a:
            return 0
        return fact[a] * invfact[b] % MOD * invfact[a - b] % MOD

    # Sum of C(i+j, i) for 0 <= i <= a, 0 <= j <= b.
    def T(a, b):
        if a < 0 or b < 0:
            return 0
        return (comb(a + b + 2, a + 1) - 1) % MOD

    # Sum of unrestricted path counts ending in 0 <= x <= a, 0 <= y <= b.
    # This is also the double prefix sum of T.
    def Q(a, b):
        if a < 0 or b < 0:
            return 0
        return (
            comb(a + b + 4, a + 2)
            - (a + 3)
            - (a + 2) * (b + 1)
        ) % MOD

    def F(x, y):
        if x < 0 or y < 0:
            return 0
        return (comb(x + y + 2, x + 1) - 1) % MOD

    # Sum of T(a,b) over a1 <= a <= a2 and b1 <= b <= b2.
    def rect_sum_t(a1, a2, b1, b2):
        if a1 > a2 or b1 > b2:
            return 0
        return (
            Q(a2, b2)
            - Q(a1 - 1, b2)
            - Q(a2, b1 - 1)
            + Q(a1 - 1, b1 - 1)
        ) % MOD

    # First count all unrestricted paths whose endpoint is allowed.
    total = Q(W, H)
    forbidden_endpoints = (
        Q(R, U)
        - Q(L - 1, U)
        - Q(R, D - 1)
        + Q(L - 1, D - 1)
    ) % MOD
    answer = (total - forbidden_endpoints) % MOD

    # Number of continuations from a forbidden vertex (zx, zy) to allowed
    # endpoints. The endpoint regions strictly right of, and strictly above,
    # the forbidden rectangle are disjoint.
    def continuation_sum(zx, zy):
        right = (
            T(W - zx, H - zy)
            - T(R - zx, H - zy)
        ) % MOD

        top = (
            T(R - zx, H - zy)
            - T(R - zx, U - zy)
        ) % MOD

        return (right + top) % MOD

    bad = 0

    # First entry through the bottom side, using only prefixes that were
    # entirely allowed before the first forbidden vertex.
    for x in range(L, R + 1):
        ways = F(x, D - 1)
        if x == L:
            ways += F(L - 1, D)
        bad = (bad + ways * continuation_sum(x, D)) % MOD

    # First entry through the left side, excluding the bottom-left corner.
    for y in range(D + 1, U + 1):
        ways = F(L - 1, y)
        bad = (bad + ways * continuation_sum(L, y)) % MOD

    # Paths whose starting block is already forbidden. The zero-length prefix
    # contributes one for every forbidden starting vertex, including all
    # boundary vertices. Sum their continuation counts in closed form.
    #
    # For starts (x,y) in the forbidden rectangle:
    #   right contribution: T(W-x,H-y) - T(R-x,H-y)
    #   top contribution:   T(R-x,H-y) - T(R-x,U-y)
    # The middle terms cancel after summing.
    starts_right = rect_sum_t(
        W - R, W - L,
        H - U, H - D
    )
    starts_top_subtracted = rect_sum_t(
        0, R - L,
        0, U - D
    )
    bad = (bad + starts_right - starts_top_subtracted) % MOD

    answer = (answer - bad) % MOD
    print(answer)


if __name__ == "__main__":
    solve()