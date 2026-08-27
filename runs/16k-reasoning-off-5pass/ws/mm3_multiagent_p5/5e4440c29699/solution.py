import sys

MOD = 998244353

def solve():
    W, H, L, R, D, U = map(int, sys.stdin.readline().split())
    max_n = W + H + 10
    fact = [1] * (max_n + 1)
    for i in range(1, max_n + 1):
        fact[i] = fact[i-1] * i % MOD
    inv_fact = [1] * (max_n + 1)
    inv_fact[max_n] = pow(fact[max_n], MOD-2, MOD)
    for i in range(max_n, 0, -1):
        inv_fact[i-1] = inv_fact[i] * i % MOD

    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        return fact[n] * inv_fact[r] % MOD * inv_fact[n-r] % MOD

    def f_full(w, h):
        if w < 0 or h < 0:
            return 0
        # f_full(w,h) = C(w+h+4, w+2) - w - h - 4 - (w+1)(h+1)
        res = nCr(w+h+4, w+2)
        res = (res - w - h - 4) % MOD
        res = (res - (w+1)*(h+1)) % MOD
        return res

    def S(x, y):
        # S(x,y) = sum_{i=0..x} sum_{j=0..y} C(i+j+2, i+1)
        if x < 0 or y < 0:
            return 0
        # S(x,y) = C(x+y+4, x+2) - x - y - 4
        res = nCr(x+y+4, x+2)
        res = (res - x - y - 4) % MOD
        return res

    full = f_full(W, H)
    N = (R - L + 1) * (U - D + 1) % MOD

    # Sum1 = sum_{x=L..R} sum_{y=D..U} C(x+y+2, x+1)
    Sum1 = (S(R, U) - S(L-1, U) - S(R, D-1) + S(L-1, D-1)) % MOD

    # Sum2 = sum_{x'=W-R..W-L} sum_{y'=H-U..H-D} C(x'+y'+2, x'+1)
    # x' from W-R to W-L, y' from H-U to H-D
    Sum2 = (S(W-L, H-D) - S(W-R-1, H-D) - S(W-L, H-U-1) + S(W-R-1, H-U-1)) % MOD

    rect = f_full(R-L, U-D)

    ans = (full - Sum1 - Sum2 + 2 * N + rect) % MOD
    print(ans)

solve()