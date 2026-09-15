import sys

MOD = 998244353


def main():
    W, H, L, R, D, U = map(int, sys.stdin.buffer.read().split())

    # Maximum factorial index needed is W + H + 4.
    N = W + H + 5
    mod = MOD

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % mod

    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], mod - 2, mod)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % mod

    def C(n, k):
        if k < 0 or k > n:
            return 0
        return fact[n] * invfact[k] % mod * invfact[n - k] % mod

    # P(n, m) = sum_{0 <= i <= n, 0 <= j <= m} C(i+j+2, i+1)
    def P(n, m):
        if n < 0 or m < 0:
            return 0
        return (C(n + m + 4, n + 2) - n - m - 4) % mod

    def sum_binom_rect(i1, i2, j1, j2):
        if i1 > i2 or j1 > j2:
            return 0
        return (
            P(i2, j2)
            - P(i1 - 1, j2)
            - P(i2, j1 - 1)
            + P(i1 - 1, j1 - 1)
        ) % mod

    # Sum of suffix_sum(x, y) over x in [x1, x2], y in [y1, y2],
    # where suffix_sum(x, y) is the number of monotone paths from (x, y)
    # to any point in the full W x H grid.
    def sum_suffix_rect(x1, x2, y1, y2):
        if x1 > x2 or y1 > y2:
            return 0
        i1 = W - x2
        i2 = W - x1
        j1 = H - y2
        j2 = H - y1
        area = ((x2 - x1 + 1) * (y2 - y1 + 1)) % mod
        return (sum_binom_rect(i1, i2, j1, j2) - area) % mod

    # Total number of monotone paths in the full grid, including length 0.
    total = (C(W + H + 4, W + 2) - (H + 3) - (W + 1) * (H + 2)) % mod

    # Invalid paths: paths that visit the forbidden rectangle at least once.
    # Case 1: the path starts inside the forbidden rectangle.
    invalid = sum_suffix_rect(L, R, D, U)

    f = fact
    inv = invfact

    # Case 2: first forbidden point is entered from below, on y = D.
    if D > 0:
        invD = inv[D]
        invHD1 = inv[H - D + 1]
        D1 = D + 1
        W1 = W + 1
        base = W + H - D + 2
        s = 0
        for x in range(L, R + 1):
            # Paths from any start with y < D to (x, D-1).
            pref = (f[x + D1] * inv[x + 1] * invD) % mod - 1
            # Paths from (x, D) to any endpoint.
            suff = (f[base - x] * inv[W1 - x] * invHD1) % mod - 1
            s += pref * suff
        invalid = (invalid + s) % mod

    # Case 3: first forbidden point is entered from the left, on x = L.
    if L > 0:
        invL = inv[L]
        kconst = W - L + 1
        invK = inv[kconst]
        base = W - L + H + 2
        s = 0
        for y in range(D, U + 1):
            # Paths from any start with x < L to (L-1, y).
            pref = (f[L + y + 1] * invL * inv[y + 1]) % mod - 1
            # Paths from (L, y) to any endpoint.
            suff = (f[base - y] * invK * inv[H - y + 1]) % mod - 1
            s += pref * suff
        invalid = (invalid + s) % mod

    ans = (total - invalid) % mod
    sys.stdout.write(str(ans))


if __name__ == "__main__":
    main()