import sys

MOD = 998244353

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    W = int(next(it))
    H = int(next(it))
    L = int(next(it))
    R = int(next(it))
    D = int(next(it))
    U = int(next(it))
    
    # Precompute factorials up to W+H+5 (enough for all binomials)
    max_n = W + H + 10
    fact = [1] * (max_n)
    inv_fact = [1] * (max_n)
    for i in range(1, max_n):
        fact[i] = fact[i-1] * i % MOD
    inv_fact[max_n-1] = pow(fact[max_n-1], MOD-2, MOD)
    for i in range(max_n-2, -1, -1):
        inv_fact[i] = inv_fact[i+1] * (i+1) % MOD
    
    def C(n, k):
        if k < 0 or k > n:
            return 0
        return fact[n] * inv_fact[k] % MOD * inv_fact[n-k] % MOD
    
    # Total paths in full rectangle [0,W]x[0,H]
    # T = C(W+H+4, W+2) - (W+1)*(H+1) - W - H - 4
    T = (C(W+H+4, W+2) - (W+1)*(H+1) - W - H - 4) % MOD
    
    # g(x,y): number of paths from (x,y) to any end in full rectangle
    # g(x,y) = C((W-x)+(H-y)+2, W-x+1) - 1
    def g(x, y):
        return (C(W - x + H - y + 2, W - x + 1) - 1) % MOD
    
    # f(L-1, y) = C(L+y+1, L) - 1  (valid paths to (L-1, y))
    def f_left(y):
        return (C(L + y + 1, L) - 1) % MOD
    
    # f(x, D-1) = C(x+D+1, x+1) - 1  (valid paths to (x, D-1))
    def f_bottom(x):
        return (C(x + D + 1, x + 1) - 1) % MOD
    
    I = 0
    if L > 0 and D > 0:
        # Left boundary: entry at (L, y) for y in [D, U]
        s1 = 0
        for y in range(D, U+1):
            s1 = (s1 + f_left(y) * g(L, y)) % MOD
        # Bottom boundary: entry at (x, D) for x in [L, R]
        s2 = 0
        for x in range(L, R+1):
            s2 = (s2 + f_bottom(x) * g(x, D)) % MOD
        I = (s1 + s2) % MOD
    elif L == 0 and D > 0:
        # Left side: paths starting in hole at (0, y)
        s1 = 0
        for y in range(D, U+1):
            s1 = (s1 + g(0, y)) % MOD
        # Bottom boundary: entry at (x, D) for x in [0, R]
        s2 = 0
        for x in range(0, R+1):
            s2 = (s2 + f_bottom(x) * g(x, D)) % MOD
        I = (s1 + s2) % MOD
    elif L > 0 and D == 0:
        # Left boundary: entry at (L, y) for y in [0, U]
        s1 = 0
        for y in range(0, U+1):
            s1 = (s1 + f_left(y) * g(L, y)) % MOD
        # Bottom side: paths starting in hole at (x, 0)
        s2 = 0
        for x in range(L, W+1):
            s2 = (s2 + g(x, 0)) % MOD
        I = (s1 + s2) % MOD
    else:  # L == 0 and D == 0
        # All invalid paths start in the hole; avoid double count at (0,0)
        s1 = 0
        for y in range(0, U+1):
            s1 = (s1 + g(0, y)) % MOD
        s2 = 0
        for x in range(0, R+1):
            s2 = (s2 + g(x, 0)) % MOD
        I = (s1 + s2 - g(0, 0)) % MOD
    
    ans = (T - I) % MOD
    print(ans)

if __name__ == "__main__":
    main()