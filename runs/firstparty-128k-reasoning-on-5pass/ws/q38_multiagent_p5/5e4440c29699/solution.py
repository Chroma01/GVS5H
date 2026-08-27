import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    W, H, L, R, D, U = map(int, data)
    del data

    mod = MOD
    N = W + H + 4

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % mod

    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], mod - 2, mod)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % mod

    def S(A, B, f=fact, inv=invfact, md=mod):
        if A < 0 or B < 0:
            return 0
        n = A + B + 4
        k = A + 2
        c = (f[n] * inv[k] * inv[n - k]) % md
        return (c - A - B - 4 - (A + 1) * (B + 1)) % md

    total = S(W, H)

    a1 = W - R
    a2 = W - L
    b1 = H - U
    b2 = H - D
    rect = (S(a2, b2) - S(a1 - 1, b2) - S(a2, b1 - 1) + S(a1 - 1, b1 - 1)) % mod
    total_allowed = (total - rect) % mod

    bad_below = 0
    if D > 0:
        m = R - L + 1
        total_x = W + 1
        f = fact
        inv = invfact
        invD = inv[D]
        invHmD1 = inv[H - D + 1]
        base = W + H - D + 2

        if m <= total_x - m:
            s = 0
            for x in range(L, R + 1):
                c1 = (f[x + D + 1] * invD * inv[x + 1]) % mod
                c2 = (f[base - x] * invHmD1 * inv[W - x + 1]) % mod
                s += (c1 - 1) * (c2 - 1)
            bad_below = s % mod
        else:
            full = (total - S(W, D - 1) - S(W, H - D)) % mod
            s = 0
            for x in range(0, L):
                c1 = (f[x + D + 1] * invD * inv[x + 1]) % mod
                c2 = (f[base - x] * invHmD1 * inv[W - x + 1]) % mod
                s += (c1 - 1) * (c2 - 1)
            for x in range(R + 1, W + 1):
                c1 = (f[x + D + 1] * invD * inv[x + 1]) % mod
                c2 = (f[base - x] * invHmD1 * inv[W - x + 1]) % mod
                s += (c1 - 1) * (c2 - 1)
            bad_below = (full - s) % mod

    bad_left = 0
    if L > 0:
        m = U - D + 1
        total_y = H + 1
        f = fact
        inv = invfact
        invL = inv[L]
        invWmL1 = inv[W - L + 1]
        base = W - L + H + 2

        if m <= total_y - m:
            s = 0
            for y in range(D, U + 1):
                c1 = (f[L + y + 1] * invL * inv[y + 1]) % mod
                c2 = (f[base - y] * invWmL1 * inv[H - y + 1]) % mod
                s += (c1 - 1) * (c2 - 1)
            bad_left = s % mod
        else:
            full = (total - S(L - 1, H) - S(W - L, H)) % mod
            s = 0
            for y in range(0, D):
                c1 = (f[L + y + 1] * invL * inv[y + 1]) % mod
                c2 = (f[base - y] * invWmL1 * inv[H - y + 1]) % mod
                s += (c1 - 1) * (c2 - 1)
            for y in range(U + 1, H + 1):
                c1 = (f[L + y + 1] * invL * inv[y + 1]) % mod
                c2 = (f[base - y] * invWmL1 * inv[H - y + 1]) % mod
                s += (c1 - 1) * (c2 - 1)
            bad_left = (full - s) % mod

    ans = (total_allowed - bad_below - bad_left) % mod
    print(ans)

if __name__ == "__main__":
    main()