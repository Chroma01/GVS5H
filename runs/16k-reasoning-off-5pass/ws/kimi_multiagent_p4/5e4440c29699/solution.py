import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    W, H, L, R, D, U = map(int, data[:6])

    N = W + H + 5
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    ifac = [1] * (N + 1)
    ifac[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        ifac[i - 1] = ifac[i] * i % MOD

    def C(n, k):
        if k < 0 or k > n or n < 0:
            return 0
        return fact[n] * ifac[k] % MOD * ifac[n - k] % MOD

    def S(X, Y):
        # sum_{x=0..X, y=0..Y} C(x+y, x) = C(X+Y+2, X+1) - 1
        if X < 0 or Y < 0:
            return 0
        return (C(X + Y + 2, X + 1) - 1) % MOD

    def G(X, Y):
        # sum_{x=0..X, y=0..Y} S(x, y)
        if X < 0 or Y < 0:
            return 0
        return (C(X + Y + 4, X + 2) - (X + 1) * (Y + 1) - X - Y - 4) % MOD

    # Sum of S(p) over all blocks = G(W,H) - sum over hole
    ans = (G(W, H) - G(R, U) + G(L - 1, U) + G(R, D - 1) - G(L - 1, D - 1)) % MOD

    # Subtract sum over hole points q of c(q) * (paths q -> block p)
    # c(q) = 1 + [qx==L]*S(L-1,qy) + [qy==D]*S(qx,D-1)

    # Part from c(q)'s "1": sum_{q in hole} [S(W-qx,H-qy) - S(R-qx,U-qy)]
    ones = (G(W - L, H - D) - G(W - R - 1, H - D)
            - G(W - L, H - U - 1) + G(W - R - 1, H - U - 1)
            - G(R - L, U - D)) % MOD
    ans = (ans - ones) % MOD

    # Left edge: qx = L, qy = D..U, weight S(L-1, qy)
    if L >= 1:
        a = W - L
        b = R - L
        sub = 0
        for qy in range(D, U + 1):
            w = S(L - 1, qy)
            t = (S(a, H - qy) - S(b, U - qy)) % MOD
            sub = (sub + w * t) % MOD
        ans = (ans - sub) % MOD

    # Bottom edge: qy = D, qx = L..R, weight S(qx, D-1)
    if D >= 1:
        hd = H - D
        ud = U - D
        sub = 0
        for qx in range(L, R + 1):
            w = S(qx, D - 1)
            t = (S(W - qx, hd) - S(R - qx, ud)) % MOD
            sub = (sub + w * t) % MOD
        ans = (ans - sub) % MOD

    print(ans % MOD)

main()