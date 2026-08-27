import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    W, H, L, R, D, U = map(int, data[:6])

    # Factorials up to W+H+4 (largest binomial argument is C(W+H+4, ...) in S).
    N = W + H + 5
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def C(n, k):
        if k < 0 or k > n or n < 0:
            return 0
        return fact[n] * invfact[k] % MOD * invfact[n - k] % MOD

    def S(w, h):
        # Total monotone paths (any length >= 0) inside a (w+1) x (h+1) rectangle of points.
        if w < 0 or h < 0:
            return 0
        return (C(w + h + 4, h + 2) - (w + h + 4) - (w + 1) * (h + 1)) % MOD

    q = U - D
    ans = 0
    # Paths staying in one region:
    # B: [0,W]x[0,D-1], L: [0,L-1]x[D,U], R: [R+1,W]x[D,U], T: [0,W]x[U+1,H]
    ans += S(W, D - 1)
    ans += S(L - 1, q)
    ans += S(W - R - 1, q)
    ans += S(W, H - U - 1)
    ans %= MOD

    # B->L: crossing edge (x,D-1)->(x,D), x in [0,L-1]
    for x in range(0, L):
        a = (C(x + D + 1, D) - 1) % MOD
        p = (C((L - 1 - x) + q + 2, q + 1) - 1) % MOD
        ans = (ans + a * p) % MOD
    # B->R: crossing edge (x,D-1)->(x,D), x in [R+1,W]
    for x in range(R + 1, W + 1):
        a = (C(x + D + 1, D) - 1) % MOD
        p = (C((W - x) + q + 2, q + 1) - 1) % MOD
        ans = (ans + a * p) % MOD
    # L->T: crossing edge (x,U)->(x,U+1), x in [0,L-1]
    for x in range(0, L):
        a = (C(x + q + 2, x + 1) - 1) % MOD
        c = (C((W - x) + (H - U - 1) + 2, (W - x) + 1) - 1) % MOD
        ans = (ans + a * c) % MOD
    # R->T: crossing edge (x,U)->(x,U+1), x in [R+1,W]
    for x in range(R + 1, W + 1):
        a = (C((x - R - 1) + q + 2, (x - R - 1) + 1) - 1) % MOD
        c = (C((W - x) + (H - U - 1) + 2, (W - x) + 1) - 1) % MOD
        ans = (ans + a * c) % MOD
    # B->L->T: e1 at x1 in [0,L-1], e2 at x2 in [x1,L-1]
    # G(x2) = C(x2+U+2, U+1) - C(x2+U-D+2, U-D+1)  (Vandermonde convolution)
    for x2 in range(0, L):
        G = (C(x2 + U + 2, U + 1) - C(x2 + U - D + 2, U - D + 1)) % MOD
        cT = (C((W - x2) + (H - U - 1) + 2, (W - x2) + 1) - 1) % MOD
        ans = (ans + G * cT) % MOD
    # B->R->T: e1 at x1 in [R+1,W], e2 at x2 in [x1,W]
    # G_R(x2) = C(x2+U+2, U+1) - C(x2+U-D-R, U-D+1)
    for x2 in range(R + 1, W + 1):
        G = (C(x2 + U + 2, U + 1) - C(x2 + U - D - R, U - D + 1)) % MOD
        cT = (C((W - x2) + (H - U - 1) + 2, (W - x2) + 1) - 1) % MOD
        ans = (ans + G * cT) % MOD

    print(ans % MOD)

main()