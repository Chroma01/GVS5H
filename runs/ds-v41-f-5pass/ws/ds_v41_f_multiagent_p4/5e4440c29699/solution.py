import sys

def main():
    data = sys.stdin.buffer.read().split()
    W, H, L, R, D, U = (int(x) for x in data[:6])
    MOD = 998244353
    maxn = W + H + 4

    fact = [1] * (maxn + 1)
    for i in range(1, maxn + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (maxn + 1)
    invfact[maxn] = pow(fact[maxn], MOD - 2, MOD)
    for i in range(maxn, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD
    inv = [0] * (maxn + 1)
    if maxn >= 1:
        inv[1] = 1
    for i in range(2, maxn + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    def C(n, k):
        if n < 0 or k < 0 or k > n:
            return 0
        return fact[n] * invfact[k] % MOD * invfact[n - k] % MOD

    # Pprefix(X,Y) = sum_{x=0..X} sum_{y=0..Y} C(x+y+2, x+1)
    def Pprefix(X, Y):
        if X < 0 or Y < 0:
            return 0
        return (C(X + Y + 4, X + 2) - (X + Y + 4)) % MOD

    # sum of f_full over whole grid, f_full(x,y)=C(x+y+2,x+1)-1
    total_grid = (Pprefix(W, H) - (W + 1) * (H + 1)) % MOD

    # sum of f_full over forbidden rectangle F=[L,R]x[D,U]
    Pf = (Pprefix(R, U) - Pprefix(L - 1, U) - Pprefix(R, D - 1) + Pprefix(L - 1, D - 1)) % MOD
    areaF = (R - L + 1) * (U - D + 1) % MOD
    sumF_ffull = (Pf - areaF) % MOD

    sum_valid_ffull = (total_grid - sumF_ffull) % MOD

    # sum over F of W(c)=S(c)-R(c)
    sumS = (Pprefix(W - L, H - D) - Pprefix(W - R - 1, H - D)
            - Pprefix(W - L, H - U - 1) + Pprefix(W - R - 1, H - U - 1)) % MOD
    sumR = Pprefix(R - L, U - D) % MOD
    sumF_W = (sumS - sumR) % MOD

    # Term2: [L>=1] * sum_{y=D..U} f_full(L-1,y) * W(L,y)
    Term2 = 0
    if L >= 1:
        c1 = C(L + D + 1, L)                              # C(L+y+1,L)
        c2 = C((W - L) + (H - D) + 2, W - L + 1)          # C((W-L)+(H-y)+2, W-L+1)
        c3 = C((R - L) + (U - D) + 2, R - L + 1)          # C((R-L)+(U-y)+2, R-L+1)
        k2 = W - L + 1
        k3 = R - L + 1
        A = W - L + H + 2
        B = R - L + U + 2
        acc = 0
        for y in range(D, U + 1):
            ff = c1 - 1
            Wv = c2 - c3
            acc = (acc + ff * Wv) % MOD
            if y < U:
                c1 = c1 * (L + y + 2) % MOD * inv[y + 2] % MOD
                n2 = A - y
                c2 = c2 * (n2 - k2) % MOD * inv[n2] % MOD
                n3 = B - y
                c3 = c3 * (n3 - k3) % MOD * inv[n3] % MOD
        Term2 = acc

    # Term3: [D>=1] * sum_{x=L..R} f_full(x,D-1) * W(x,D)
    Term3 = 0
    if D >= 1:
        c1 = C(L + D + 1, L + 1)                          # C(x+D+1,x+1)
        c2 = C((W - L) + (H - D) + 2, W - L + 1)
        c3 = C((R - L) + (U - D) + 2, R - L + 1)
        acc = 0
        for x in range(L, R + 1):
            ff = c1 - 1
            Wv = c2 - c3
            acc = (acc + ff * Wv) % MOD
            if x < R:
                c1 = c1 * (x + D + 2) % MOD * inv[x + 2] % MOD
                n2 = W + H - D + 2 - x
                c2 = c2 * (W - x + 1) % MOD * inv[n2] % MOD
                n3 = R + U - D + 2 - x
                c3 = c3 * (R - x + 1) % MOD * inv[n3] % MOD
        Term3 = acc

    sumHW = (sumF_W + Term2 + Term3) % MOD
    ans = (sum_valid_ffull - sumHW) % MOD
    print(ans % MOD)

main()