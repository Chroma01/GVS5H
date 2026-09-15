import sys

def main():
    data = sys.stdin.buffer.read().split()
    W, H, L, R, D, U = map(int, data[:6])
    MOD = 998244353
    N = W + H + 6

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i-1] * i % MOD

    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        inv_fact[i-1] = inv_fact[i] * i % MOD

    f = fact
    inv = inv_fact

    def C(n, k):
        if k < 0 or k > n or n < 0:
            return 0
        return f[n] * inv[k] % MOD * inv[n-k] % MOD

    # Total walks over the entire (W+1)x(H+1) grid.
    T = (C(W+H+4, H+2) - (H+3) - (W+1)*(H+2)) % MOD

    # 2D prefix of g over "distance" coordinates: F(I,J) = sum_{I'<=I,J'<=J} g-combinatoric part
    def F(I, J):
        if I < 0 or J < 0:
            return 0
        return (C(I+J+4, J+2) - (J+3) - (I+1)) % MOD

    i1, i2 = W - R, W - L
    j1, j2 = H - U, H - D
    SumC = (F(i2, j2) - F(i1-1, j2) - F(i2, j1-1) + F(i1-1, j1-1)) % MOD
    StartTerm = (SumC - (R-L+1)*(U-D+1)) % MOD

    # term A: first hole entry from below, only if D >= 1
    TermA = 0
    if D >= 1:
        hd1 = H - D + 1
        invD = inv[D]
        invHD1 = inv[hd1]
        for x in range(L, R+1):
            c1 = f[x+D+1] * invD % MOD * inv[x+1] % MOD
            c2 = f[W-x+H-D+2] * invHD1 % MOD * inv[W-x+1] % MOD
            TermA = (TermA + (c1-1)*(c2-1)) % MOD

    # term B: first hole entry from left, only if L >= 1
    TermB = 0
    if L >= 1:
        wl1 = W - L + 1
        invL = inv[L]
        invWL1 = inv[wl1]
        for y in range(D, U+1):
            c1 = f[L+y+1] * invL % MOD * inv[y+1] % MOD
            c2 = f[W-L+H-y+2] * invWL1 % MOD * inv[H-y+1] % MOD
            TermB = (TermB + (c1-1)*(c2-1)) % MOD

    ans = (T - StartTerm - TermA - TermB) % MOD
    print(ans % MOD)

main()