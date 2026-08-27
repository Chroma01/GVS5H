import sys

MOD = 998244353

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    W, H, L, R, D, U = map(int, data)

    # ---------- pre‑compute factorials ----------
    max_n = W + H + 5          # safe upper bound for all binomials
    fact = [1] * (max_n + 1)
    for i in range(1, max_n + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (max_n + 1)
    inv_fact[max_n] = pow(fact[max_n], MOD - 2, MOD)
    for i in range(max_n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    def C(n: int, k: int) -> int:
        if k < 0 or k > n:
            return 0
        return fact[n] * inv_fact[k] % MOD * inv_fact[n - k] % MOD

    # helper: full[x][y] for the full board
    def full(x: int, y: int) -> int:
        dx = W - x
        dy = H - y
        return (C(dx + dy + 2, dx + 1) - 1) % MOD

    # ---------- TOTAL : sum of full over the whole board ----------
    total = (C(W + H + 4, W + 2) - (W + H + 4) - (W + 1) * (H + 1)) % MOD

    # ---------- sum of full over the forbidden rectangle ----------
    blocked = 0
    rows = U - D + 1
    a = H - U          # smallest t = H - j
    b = H - D          # largest  t = H - j
    for i in range(L, R + 1):
        dx = W - i
        # sum_{j=D}^{U} C(dx + (H-j) + 2 , dx + 1)
        # = C(dx+b+3,dx+2) - C(dx+a+2,dx+2)
        sumC = (C(dx + b + 3, dx + 2) - C(dx + a + 2, dx + 2)) % MOD
        blocked = (blocked + sumC - rows) % MOD

    # ---------- paths that first enter the rectangle ----------
    # left side (x = L)
    Sleft = 0
    if L > 0:                 # otherwise no neighbour to the left
        for j in range(D, U + 1):
            leftCnt = (C(L + j + 1, L) - 1) % MOD
            dp_after = full(L, j)
            Sleft = (Sleft + leftCnt * dp_after) % MOD

    # bottom side (y = D)
    Sbottom = 0
    if D > 0:                 # otherwise no neighbour below
        for i in range(L, R + 1):
            bottomCnt = (C(i + D + 1, i + 1) - 1) % MOD
            dp_after = full(i, D)
            Sbottom = (Sbottom + bottomCnt * dp_after) % MOD

    # ---------- final answer ----------
    ans = (total - blocked - Sleft - Sbottom) % MOD
    print(ans)


if __name__ == "__main__":
    solve()