import sys

def main():
    MOD = 998244353
    data = sys.stdin.read().split()
    if not data:
        return
    W, H, L, R, D, U = map(int, data)

    maxN = W + H + 5
    fact = [1] * (maxN + 1)
    for i in range(1, maxN + 1):
        fact[i] = fact[i-1] * i % MOD

    invfact = [1] * (maxN + 1)
    invfact[maxN] = pow(fact[maxN], MOD - 2, MOD)
    for i in range(maxN, 0, -1):
        invfact[i-1] = invfact[i] * i % MOD

    def sumN(X, Y):
        if X < 0 or Y < 0:
            return 0
        n = X + Y + 4
        k = X + 2
        comb = fact[n] * invfact[k] % MOD * invfact[n - k] % MOD
        return (comb - n - (X + 1) * (Y + 1)) % MOD

    full = sumN(W, H)
    e1 = (sumN(R, U) - sumN(L - 1, U) - sumN(R, D - 1) + sumN(L - 1, D - 1)) % MOD

    e2 = 0
    if R < W:
        A = W - R - 1
        base1 = R + 2
        base2 = A + H + 2
        invR1 = invfact[R + 1]
        invA1 = invfact[A + 1]
        total = 0
        f = fact
        invf = invfact
        for b in range(D, U + 1):
            c1 = (f[base1 + b] * invR1 * invf[b + 1]) % MOD
            c2 = (f[base2 - b] * invA1 * invf[H + 1 - b]) % MOD
            total += (c1 - 1) * (c2 - 1)
        e2 = total % MOD

    e3 = 0
    if U < H:
        B = H - U - 1
        base1 = U + 2
        base2 = B + 2
        invU1 = invfact[U + 1]
        invB1 = invfact[B + 1]
        total = 0
        f = fact
        invf = invfact
        for a in range(L, R + 1):
            c1 = (f[a + base1] * invf[a + 1] * invU1) % MOD
            c2 = (f[W - a + base2] * invB1 * invf[W - a + 1]) % MOD
            total += (c1 - 1) * (c2 - 1)
        e3 = total % MOD

    ans = (full - e1 - e2 - e3) % MOD
    print(ans)

if __name__ == "__main__":
    main()