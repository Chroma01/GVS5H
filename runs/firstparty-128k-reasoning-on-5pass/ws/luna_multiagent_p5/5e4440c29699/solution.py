import sys

MOD = 998244353


def main():
    W, H, L, R, D, U = map(int, sys.stdin.buffer.read().split())

    nmax = W + H + 5
    fact = [1] * (nmax + 1)
    for i in range(1, nmax + 1):
        fact[i] = fact[i - 1] * i % MOD

    ifact = [1] * (nmax + 1)
    ifact[nmax] = pow(fact[nmax], MOD - 2, MOD)
    for i in range(nmax, 0, -1):
        ifact[i - 1] = ifact[i] * i % MOD

    def comb(n, k):
        if n < 0 or k < 0 or k > n:
            return 0
        return fact[n] * ifact[k] % MOD * ifact[n - k] % MOD

    def f0(x, y):
        if x < 0 or y < 0:
            return 0
        return (comb(x + y + 2, x + 1) - 1) % MOD

    # Sum of f0 over the whole unrestricted grid.
    total = (
        comb(W + H + 4, W + 2)
        - (W + H + 4)
        - (W + 1) * (H + 1)
    ) % MOD

    # Remove endpoints inside the forbidden rectangle.
    rect_sum = (
        comb(R + U + 4, U + 2)
        - comb(L + U + 3, U + 2)
        - comb(R + D + 3, D + 1)
        + comb(L + D + 2, D + 1)
        - (R - L + 1) * (U - D + 1)
    ) % MOD

    ans = (total - rect_sum) % MOD

    # E: L <= x <= R, y > U.
    # A path entering this region is corrected from the lower boundary y = U.
    B = H - U
    corr_e = 0
    for x in range(L, R + 1):
        p = R - x
        ways = comb(p + B + 1, p + 1) - 1
        corr_e = (corr_e + f0(x, U) * ways) % MOD
    ans = (ans - corr_e) % MOD

    # F: x > R, D <= y <= U.
    # A path entering this region is corrected from the left boundary x = R.
    A = W - R
    corr_f = 0
    for y in range(D, U + 1):
        q = U - y
        ways = comb(A + q + 1, A) - 1
        corr_f = (corr_f + f0(R, y) * ways) % MOD
    ans = (ans - corr_f) % MOD

    # G: x > R, y > U.
    # Contributions from the upper strip boundary x = R and
    # the right strip boundary y = U are both needed.
    corr_g_left = 0
    for x in range(L, R + 1):
        p = R - x
        ways = (
            comb(p + A + B + 1, p + A + 1)
            - comb(p + B + 1, p + 1)
        )
        corr_g_left = (corr_g_left + f0(x, U) * ways) % MOD

    corr_g_bottom = 0
    for y in range(D, U + 1):
        q = U - y
        ways = (
            comb(A + q + B + 1, q + B + 1)
            - comb(A + q + 1, q + 1)
        )
        corr_g_bottom = (corr_g_bottom + f0(R, y) * ways) % MOD

    ans = (ans - corr_g_left - corr_g_bottom) % MOD
    print(ans)


if __name__ == "__main__":
    main()