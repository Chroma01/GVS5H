import sys

MOD = 998244353


def solve_fast(W, H, L, R, D, U):
    N = W + H + 8
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

    def T0(a, b):
        # sum_{x=0..a, y=0..b} (C(x+y+2, x+1) - 1); 0 if a<0 or b<0
        if a < 0 or b < 0:
            return 0
        return (C(a + b + 4, b + 2) - (b + 3) - (a + 1) - (a + 1) * (b + 1)) % MOD

    # Base: sum of g0 over all blocks (rect minus hole)
    base = (T0(W, H)
            - (T0(R, U) - T0(L - 1, U) - T0(R, D - 1) + T0(L - 1, D - 1))) % MOD

    # HoleStartSum: paths whose start is inside the hole, ending at a block
    hole_start = ((T0(W - L, H - D) - T0(W - R - 1, H - D)
                   - T0(W - L, H - U - 1) + T0(W - R - 1, H - U - 1))
                  - T0(R - L, U - D)) % MOD

    # EntrySum: paths entering the hole from outside (left edge / bottom edge)
    entry = 0
    if L > 0:
        for y in range(D, U + 1):
            w = (C(L + y + 1, L) - 1) % MOD            # g0(L-1, y)
            full = (C((W - L) + (H - y) + 2, W - L + 1) - 1) % MOD
            hole = (C((R - L) + (U - y) + 2, R - L + 1) - 1) % MOD
            entry = (entry + w * (full - hole)) % MOD
    if D > 0:
        for x in range(L, R + 1):
            w = (C(x + D + 1, x + 1) - 1) % MOD        # g0(x, D-1)
            full = (C((W - x) + (H - D) + 2, W - x + 1) - 1) % MOD
            hole = (C((R - x) + (U - D) + 2, R - x + 1) - 1) % MOD
            entry = (entry + w * (full - hole)) % MOD

    return (base - hole_start - entry) % MOD


def solve_brute(W, H, L, R, D, U):
    def hole(x, y):
        return L <= x <= R and D <= y <= U
    g = [[0] * (H + 1) for _ in range(W + 1)]
    ans = 0
    for y in range(H + 1):
        for x in range(W + 1):
            if hole(x, y):
                continue
            v = 1
            if x > 0:
                v += g[x - 1][y]
            if y > 0:
                v += g[x][y - 1]
            g[x][y] = v % MOD
            ans = (ans + v) % MOD
    return ans


def cross_validate():
    # Exhaustive small cases including boundary cases L=0, D=0, R=W, U=H
    for W in range(0, 7):
        for H in range(0, 7):
            for L in range(0, W + 1):
                for R in range(L, W + 1):
                    for D in range(0, H + 1):
                        for U in range(D, H + 1):
                            # require at least one block
                            if (R - L + 1) * (U - D + 1) == (W + 1) * (H + 1):
                                continue
                            f = solve_fast(W, H, L, R, D, U)
                            b = solve_brute(W, H, L, R, D, U)
                            if f != b:
                                print("MISMATCH", W, H, L, R, D, U, f, b)
                                return False
    return True


def main():
    # --- self-test / cross-validation ---
    assert cross_validate(), "exhaustive small-case validation failed"
    assert solve_fast(4, 3, 1, 2, 2, 3) == 192, "sample 1 failed"
    assert solve_fast(10, 12, 4, 6, 8, 11) == 4519189, "sample 2 failed"
    assert solve_fast(192, 25, 0, 2, 0, 9) == 675935675, "sample 3 failed"
    # ------------------------------------
    data = sys.stdin.read().split()
    W, H, L, R, D, U = map(int, data[:6])
    print(solve_fast(W, H, L, R, D, U))


if __name__ == "__main__":
    main()