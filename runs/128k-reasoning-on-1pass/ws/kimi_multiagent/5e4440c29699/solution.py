import sys

MOD = 998244353


def main() -> None:
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    W, H, L, R, D, U = data

    # All needed binomial upper arguments are <= W+H+4.
    N = W + H + 5
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def comb(n: int, k: int) -> int:
        if n < 0 or k < 0 or k > n:
            return 0
        return fact[n] * invfact[k] % MOD * invfact[n - k] % MOD

    def full_rect(a: int, b: int) -> int:
        # Number of monotone paths, including length 0, in [0,a] x [0,b].
        if a < 0 or b < 0:
            return 0
        return (comb(a + b + 4, a + 2) - (a + 1) * (b + 1) - (a + b + 4)) % MOD

    def start_count(a: int, b: int) -> int:
        # Paths starting at (0,0) and ending anywhere in [0,a] x [0,b].
        if a < 0 or b < 0:
            return 0
        return (comb(a + b + 2, a + 1) - 1) % MOD

    def pref_start_sum(a: int, b: int) -> int:
        # sum_{k=0}^b start_count(a,k), for b >= 0.
        if b < 0:
            return 0
        return (comb(a + b + 3, a + 2) - (b + 2)) % MOD

    total = full_rect(W, H)

    # Bad paths: classify by the FIRST forbidden vertex p=(x,y).
    # After the first forbidden vertex, every monotone continuation is valid,
    # because the path can never re-enter the rectangle after leaving it.
    bad = 0

    # 1) Empty prefix: the path starts inside the forbidden rectangle.
    # For fixed x, a=W-x and y=D..U means k=H-y runs over H-U..H-D.
    for x in range(L, R + 1):
        a = W - x
        bad += pref_start_sum(a, H - D) - pref_start_sum(a, H - U - 1)
    bad %= MOD

    # 2) First forbidden vertex is on the left edge x=L, entered from (L-1,y).
    if L > 0:
        a = W - L
        for y in range(D, U + 1):
            # End anywhere at (L-1,y): end_count(L-1,y).
            left_prefix = (comb(L + y + 1, L) - 1) % MOD
            suffix = start_count(a, H - y)
            bad = (bad + left_prefix * suffix) % MOD

    # 3) First forbidden vertex is on the bottom edge y=D, entered from (x,D-1).
    if D > 0:
        b = H - D
        for x in range(L, R + 1):
            # End anywhere at (x,D-1): end_count(x,D-1).
            bottom_prefix = (comb(x + D + 1, x + 1) - 1) % MOD
            suffix = start_count(W - x, b)
            bad = (bad + bottom_prefix * suffix) % MOD

    ans = (total - bad) % MOD
    print(ans)


if __name__ == "__main__":
    main()