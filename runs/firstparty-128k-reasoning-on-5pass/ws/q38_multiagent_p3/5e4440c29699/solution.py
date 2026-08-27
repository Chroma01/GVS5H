import sys

MOD = 998244353

def main():
    W, H, L, R, D, U = map(int, sys.stdin.buffer.read().split())
    mod = MOD

    N = W + H + 5
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % mod

    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], mod - 2, mod)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % mod

    def comb(n, k, f=fact, invf=invfact, m=mod):
        if k < 0 or k > n:
            return 0
        return (f[n] * invf[k] * invf[n - k]) % m

    def pref(A, B, m=mod):
        if A < 0 or B < 0:
            return 0
        return (comb(A + B + 4, B + 2) - A - B - 4) % m

    total = (comb(W + H + 4, W + 2) - (W + 2) * (H + 2) - 1) % mod

    A1 = W - R
    A2 = W - L
    B1 = H - U
    B2 = H - D

    rect = (
        pref(A2, B2)
        - pref(A1 - 1, B2)
        - pref(A2, B1 - 1)
        + pref(A1 - 1, B1 - 1)
    ) % mod
    area = (R - L + 1) * (U - D + 1)
    start_bad = (rect - area) % mod

    def boundary_sum(n1, n2, k1, k2, length, f=fact, invf=invfact, m=mod):
        ik1 = invf[k1]
        ik2 = invf[k2]
        j1 = n1 - k1
        j2 = n2 - k2
        s = 0
        for _ in range(length):
            c1 = (f[n1] * ik1 * invf[j1]) % m
            c2 = (f[n2] * ik2 * invf[j2]) % m
            s += (c1 - 1) * (c2 - 1)
            n1 += 1
            n2 -= 1
            j1 += 1
            j2 -= 1
        return s % m

    left_bad = 0
    if L > 0:
        left_bad = boundary_sum(
            L + D + 1,
            W - L + H - D + 2,
            L,
            W - L + 1,
            U - D + 1
        )

    bottom_bad = 0
    if D > 0:
        bottom_bad = boundary_sum(
            L + D + 1,
            W - L + H - D + 2,
            D,
            H - D + 1,
            R - L + 1
        )

    ans = (total - start_bad - left_bad - bottom_bad) % mod
    print(ans)

if __name__ == "__main__":
    main()