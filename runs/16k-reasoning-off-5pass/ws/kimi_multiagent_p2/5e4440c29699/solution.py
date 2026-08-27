import sys

def main():
    MOD = 998244353
    data = sys.stdin.read().split()
    W, H, L, R, D, U = map(int, data)

    N = W + H + 4
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    invf = [1] * (N + 1)
    invf[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invf[i - 1] = invf[i] * i % MOD

    def C(n, k):
        if k < 0 or k > n:
            return 0
        return fact[n] * invf[k] % MOD * invf[n - k] % MOD

    # F(a,b) = sum_{i=0..a} sum_{j=0..b} C(i+j+2, i+1)
    #        = C(a+b+4, a+2) - (a+3) - (b+1)   (hockey stick twice)
    def F(a, b):
        if a < 0 or b < 0:
            return 0
        return (C(a + b + 4, a + 2) - (a + 3) - (b + 1)) % MOD

    # G(a,b) = sum over all pairs s<=t in [0,a]x[0,b] of C(dx+dy, dx)
    #        = sum_{i,j} (C(i+j+2, i+1) - 1) = F(a,b) - (a+1)(b+1)
    def G(a, b):
        return (F(a, b) - (a + 1) * (b + 1)) % MOD

    hole = (R - L + 1) * (U - D + 1) % MOD

    # sum over s in hole of S(W-s.x, H-s.y), S(a,b) = C(a+b+2, a+1) - 1
    sumS = (F(W - L, H - D) - F(W - R - 1, H - D)
            - F(W - L, H - U - 1) + F(W - R - 1, H - U - 1) - hole) % MOD
    # sum over t in hole of S(t.x, t.y)
    sumT = (F(R, U) - F(L - 1, U) - F(R, D - 1) + F(L - 1, D - 1) - hole) % MOD

    # paths between allowed endpoints, ignoring the hole in between
    total = (G(W, H) - sumS - sumT + G(R - L, U - D)) % MOD

    # subtract paths that pass through the hole, decomposed by the unique
    # entry edge: bottom edges (x,D-1)->(x,D) for L<=x<=R,
    #             left edges (L-1,y)->(L,y) for D<=y<=U
    through = 0
    f = fact
    iv = invf
    M = MOD
    if D >= 1:
        for x in range(L, R + 1):
            # A1 = S(x, D-1) = C(x+D+1, D) - 1
            a1 = f[x + D + 1] * iv[D] % M * iv[x + 1] % M - 1
            # B1 = S(W-x, H-D) - S(R-x, U-D)
            b1 = (f[W - x + H - D + 2] * iv[W - x + 1] % M * iv[H - D + 1] % M
                  - f[R - x + U - D + 2] * iv[R - x + 1] % M * iv[U - D + 1] % M) % M
            through = (through + a1 * b1) % M
    if L >= 1:
        for y in range(D, U + 1):
            # A2 = S(L-1, y) = C(L+y+1, L) - 1
            a2 = f[L + y + 1] * iv[L] % M * iv[y + 1] % M - 1
            # B2 = S(W-L, H-y) - S(R-L, U-y)
            b2 = (f[W - L + H - y + 2] * iv[W - L + 1] % M * iv[H - y + 1] % M
                  - f[R - L + U - y + 2] * iv[R - L + 1] % M * iv[U - y + 1] % M) % M
            through = (through + a2 * b2) % M

    print((total - through) % MOD)

main()