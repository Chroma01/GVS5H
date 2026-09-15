import sys

def main():
    data = sys.stdin.buffer.read().split()
    W = int(data[0]); H = int(data[1])
    L = int(data[2]); R = int(data[3])
    D = int(data[4]); U = int(data[5])
    MOD = 998244353
    MAXN = W + H + 4
    fact = [1] * (MAXN + 1)
    for i in range(1, MAXN + 1):
        fact[i] = fact[i-1] * i % MOD
    invfact = [1] * (MAXN + 1)
    invfact[MAXN] = pow(fact[MAXN], MOD - 2, MOD)
    for i in range(MAXN, 0, -1):
        invfact[i-1] = invfact[i] * i % MOD

    def C(n, k):
        if k < 0 or k > n or n < 0:
            return 0
        return fact[n] * invfact[k] % MOD * invfact[n-k] % MOD

    def A(a, b):
        # sum_{x=0}^{a} sum_{y=0}^{b} F(x,y)
        if a < 0 or b < 0:
            return 0
        return (C(a + b + 4, a + 2) - (a + 3) - (b + 1) - (a + 1) * (b + 1)) % MOD

    total = A(W, H)
    hole = (A(R, U) - A(L - 1, U) - A(R, D - 1) + A(L - 1, D - 1)) % MOD

    SG = 0
    fct = fact; invf = invfact

    # right column of the hole: x = R, y in [D, U]
    if R < W:
        c1 = invf[R + 1]
        c2 = invf[W - R]
        base2 = W - R + H + 1
        s = 0
        for y in range(D, U + 1):
            t1 = fct[R + y + 2] * invf[y + 1] % MOD * c1 % MOD - 1
            t2 = fct[base2 - y] * invf[H - y + 1] % MOD * c2 % MOD - 1
            s += t1 * t2
        SG += s % MOD

    # top row of the hole: y = U, x in [L, R]
    if U < H:
        iU = invf[U + 1]
        iHU = invf[H - U]
        base = H - U + 1
        s = 0
        for x in range(L, R + 1):
            t1 = fct[x + U + 2] * invf[x + 1] % MOD * iU % MOD - 1
            t2 = fct[W - x + base] * invf[W - x + 1] % MOD * iHU % MOD - 1
            s += t1 * t2
        SG += s % MOD

    ans = (total - hole - SG) % MOD
    sys.stdout.write(str(ans % MOD) + "\n")

main()