import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    W, H, L, R, D, U = map(int, data)
    mod = MOD

    maxN = W + H + 4

    fact = [1] * (maxN + 1)
    for i in range(1, maxN + 1):
        fact[i] = fact[i - 1] * i % mod

    ifact = [1] * (maxN + 1)
    ifact[maxN] = pow(fact[maxN], mod - 2, mod)
    for i in range(maxN, 0, -1):
        ifact[i - 1] = ifact[i] * i % mod

    def C(n, k):
        if k < 0 or k > n:
            return 0
        return fact[n] * ifact[k] % mod * ifact[n - k] % mod

    def csum(I, J):
        if I < 0 or J < 0:
            return 0
        return (C(I + J + 2, I + 1) - I - J - 2) % mod

    total = (csum(W + 1, H + 1) - (W + 1) * (H + 1)) % mod

    area = (R - L + 1) * (U - D + 1) % mod
    s0 = (
        csum(W - L + 1, H - D + 1)
        - csum(W - R, H - D + 1)
        - csum(W - L + 1, H - U)
        + csum(W - R, H - U)
        - area
    ) % mod

    left = 0
    if L > 0:
        f = fact
        invf = ifact
        c1 = ifact[L]
        c2 = ifact[W - L + 1]
        base1 = L + D + 1
        base2 = W + H - L - D + 2
        i1 = D + 1
        i2 = H - D + 1
        for t in range(U - D + 1):
            a = f[base1 + t] * c1 * invf[i1 + t] % mod - 1
            b = f[base2 - t] * c2 * invf[i2 - t] % mod - 1
            left += a * b
        left %= mod

    bottom = 0
    if D > 0:
        f = fact
        invf = ifact
        cD = ifact[D]
        cHD = ifact[H - D + 1]
        base1 = L + D + 1
        base2 = W + H - L - D + 2
        i1 = L + 1
        i2 = W - L + 1
        for t in range(R - L + 1):
            a = f[base1 + t] * cD * invf[i1 + t] % mod - 1
            b = f[base2 - t] * cHD * invf[i2 - t] % mod - 1
            bottom += a * b
        bottom %= mod

    ans = (total - s0 - left - bottom) % mod
    print(ans)

if __name__ == "__main__":
    main()