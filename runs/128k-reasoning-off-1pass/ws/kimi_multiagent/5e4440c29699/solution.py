import sys

def main():
    MOD = 998244353
    data = sys.stdin.read().split()
    W, H, L, R, D, U = map(int, data[:6])

    N = W + H + 5
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    def C(n, k):
        if k < 0 or k > n or n < 0:
            return 0
        return fact[n] * inv_fact[k] % MOD * inv_fact[n - k] % MOD

    def g(a, b):
        # number of monotone paths from a corner of an (a+1)x(b+1) grid
        # = sum_{i=0..a} sum_{j=0..b} C(i+j, i) = C(a+b+2, a+1) - 1
        if a < 0 or b < 0:
            return 0
        return (C(a + b + 2, a + 1) - 1) % MOD

    def G(a, b):
        # sum_{i=0..a} sum_{j=0..b} g(i, j)
        if a < 0 or b < 0:
            return 0
        return (C(a + b + 4, a + 2) - (a + b + 4) - (a + 1) * (b + 1)) % MOD

    def rect_g(x1, x2, y1, y2):
        # sum_{x=x1..x2, y=y1..y2} g(W-x, H-y)
        if x1 > x2 or y1 > y2:
            return 0
        return (G(W - x1, H - y1) - G(W - x2 - 1, H - y1)
                - G(W - x1, H - y2 - 1) + G(W - x2 - 1, H - y2 - 1)) % MOD

    # Free region: points with x > R or y > U; f(p) = g(W-x, H-y) there.
    ans = (G(W, H) - rect_g(0, R, 0, U)) % MOD

    # SW L-shape: x<=R, y<=U, (x<L or y<D). f = |A|+|B|-|A∩B|+|C|+|D|.
    # |A|: stay x<=L-1, summed over x in [0,L-1], y in [0,U]
    ans = (ans + G(L - 1, H) - G(L - 1, H - U - 1)) % MOD
    # |B|: stay y<=D-1, summed over x in [0,R], y in [0,D-1]
    ans = (ans + G(W, D - 1) - G(W - R - 1, D - 1)) % MOD
    # -|A∩B|: x in [0,L-1], y in [0,D-1]
    ans = (ans - G(L - 1, D - 1)) % MOD

    # |C|: cross x=L at height y1 > U
    s = 0
    for y1 in range(U + 1, H + 1):
        ways = (g(L - 1, y1) - g(L - 1, y1 - U - 1)) % MOD
        s = (s + ways * g(W - L, H - y1)) % MOD
    ans = (ans + s) % MOD

    # |D|: cross y=D at position x1 > R
    s = 0
    for x1 in range(R + 1, W + 1):
        ways = (g(D - 1, x1) - g(D - 1, x1 - R - 1)) % MOD
        s = (s + ways * g(W - x1, H - D)) % MOD
    ans = (ans + s) % MOD

    print(ans % MOD)

main()