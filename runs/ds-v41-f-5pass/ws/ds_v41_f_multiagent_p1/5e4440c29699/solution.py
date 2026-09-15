import sys

def main():
    data = sys.stdin.buffer.read().split()
    W, H, L, R, D, U = (int(x) for x in data[:7])
    MOD = 998244353
    maxn = W + H + 5

    fact = [1] * (maxn + 1)
    for i in range(1, maxn + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (maxn + 1)
    invfact[maxn] = pow(fact[maxn], MOD - 2, MOD)
    for i in range(maxn, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def C(n, k):
        if k < 0 or k > n or n < 0:
            return 0
        return fact[n] * invfact[k] % MOD * invfact[n - k] % MOD

    # total monotone paths in the full W x H grid (all start/end pairs)
    f = (C(W + H + 4, W + 2) - (W + H + 4) - (W + 1) * (H + 1)) % MOD

    # paths whose first hole point is its own start (start inside the hole)
    a = W - R + 1
    b = W - L + 1
    c = H - U + 1
    d = H - D + 1

    def F(X, Y):
        if X < 0 or Y < 0:
            return 0
        return (C(X + Y + 2, X + 1) - 1) % MOD

    rect = (F(b, d) - F(a - 1, d) - F(b, c - 1) + F(a - 1, c - 1)) % MOD
    cnt = (R - L + 1) * (U - D + 1)
    start_in_F = (rect - cnt) % MOD

    # paths first entering the hole from the left edge at (L, y)
    left = 0
    if L >= 1:
        sA = fact[L + D + 1: L + U + 2]            # C(L+y+1, L) numerator part
        sIA = invfact[D + 1: U + 2]                # invfact[y+1]
        sB = fact[W - L + H - U + 2: W - L + H - D + 3]  # C(..., W-L+1) numerator
        sIB = invfact[H - U + 1: H - D + 2]
        sB.reverse()
        sIB.reverse()
        cA = invfact[L]
        cB = invfact[W - L + 1]
        total = 0
        for p, ia, q, ib in zip(sA, sIA, sB, sIB):
            A = p * cA % MOD * ia % MOD
            B = q * cB % MOD * ib % MOD
            total += (A - 1) * (B - 1)
        left = total % MOD

    # paths first entering the hole from the bottom edge at (x, D)
    bottom = 0
    if D >= 1:
        sA = fact[L + D + 1: R + D + 2]            # C(x+D+1, x+1) numerator
        sIA = invfact[L + 1: R + 2]                # invfact[x+1]
        sB = fact[W - R + H - D + 2: W - L + H - D + 3]  # C(..., W-x+1) numerator
        sIB = invfact[W - R + 1: W - L + 2]
        sB.reverse()
        sIB.reverse()
        cA = invfact[D]
        cB = invfact[H - D + 1]
        total = 0
        for p, ia, q, ib in zip(sA, sIA, sB, sIB):
            A = p * cA % MOD * ia % MOD
            B = q * cB % MOD * ib % MOD
            total += (A - 1) * (B - 1)
        bottom = total % MOD

    ans = (f - start_in_F - left - bottom) % MOD
    sys.stdout.write(str(ans) + "\n")

main()