import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    W, H, L, R, D, U = map(int, data[:6])

    # Maximum n needed in any binomial coefficient:
    #   total_full: a + H + 1 <= W + H + 1
    #   F: r + m2 + 1 = (Y2 + 1) + (X2 + 2) = X2 + Y2 + 3 <= W + H + 3
    #   G: lx + ly + 2 <= W + H + 2
    #   paths_from: (W - x) + (H - y) + 2 <= W + H + 2
    N = W + H + 4
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def C(n, k):
        if k < 0 or k > n or n < 0:
            return 0
        return fact[n] * invfact[k] % MOD * invfact[n - k] % MOD

    def total_full(w, h):
        # Sum over all pairs s<=t in [0,w]x[0,h] of C(dx+dy, dx)
        # = sum_{a=0}^{w} (w+1-a) * [ (h+1)C(a+h+1,a+1) - (a+1)C(a+h+1,a+2) ]
        res = 0
        for a in range(w + 1):
            g = (h + 1) * C(a + h + 1, a + 1) - (a + 1) * C(a + h + 1, a + 2)
            res = (res + (w + 1 - a) * g) % MOD
        return res

    def F(X1, X2, Y1, Y2):
        # Sum_{x=X1..X2} Sum_{y=Y1..Y2} C(x+y+2, x+1), via double hockey stick.
        def g(c):
            r = c - 2
            m1, m2 = X1 + 2, X2 + 2
            return (C(r + m2 + 1, m2) - C(r + m1, m1 - 1)) % MOD
        return (g(Y2 + 3) - g(Y1 + 2)) % MOD

    def paths_from(x, y):
        # Number of monotone paths starting at (x,y) (incl. trivial) in full grid.
        if x > W or y > H:
            return 0
        return (C((W - x) + (H - y) + 2, W - x + 1) - 1) % MOD

    total = total_full(W, H)

    # A: paths with valid start and valid end that touch the hole.
    # Decompose by last hole point l (on right edge x=R or top edge y=U)
    # and the unique exit step. G(l) = paths from any valid start to l
    # (full grid) = all starts minus hole starts.
    A = 0
    if R < W:
        for y in range(D, U + 1):
            G = (C(R + y + 2, R + 1) - C((R - L) + (y - D) + 2, R - L + 1)) % MOD
            OUT = paths_from(R + 1, y)
            A = (A + G * OUT) % MOD
    if U < H:
        for x in range(L, R + 1):
            G = (C(x + U + 2, x + 1) - C((x - L) + (U - D) + 2, x - L + 1)) % MOD
            OUT = paths_from(x, U + 1)
            A = (A + G * OUT) % MOD

    hole_pts = (R - L + 1) * (U - D + 1) % MOD
    # B: paths starting in the hole (any end).
    B = (F(W - R, W - L, H - U, H - D) - hole_pts) % MOD
    # Cc: paths ending in the hole (any start).
    Cc = (F(L, R, D, U) - hole_pts) % MOD
    # BC: paths with both endpoints in the hole.
    BC = total_full(R - L, U - D)

    ans = (total - A - B - Cc + BC) % MOD
    print(ans)

main()