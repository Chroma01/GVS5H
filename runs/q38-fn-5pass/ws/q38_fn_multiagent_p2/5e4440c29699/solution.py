import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    W, H, L, R, D, U = map(int, data)

    MOD = 998244353
    m = MOD
    N = W + H + 4

    fact = [1] * (N + 1)
    for i in range(2, N + 1):
        fact[i] = fact[i - 1] * i % m

    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], m - 2, m)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % m

    def comb(n, k, f=fact, invf=invfact, mod=m):
        if k < 0 or k > n:
            return 0
        return f[n] * invf[k] * invf[n - k] % mod

    # P(X, Y) = sum_{a=0..X} sum_{b=0..Y} C(a+b+2, a+1)
    def rect_sum(X, Y):
        if X < 0 or Y < 0:
            return 0
        return (comb(X + Y + 4, X + 2) - X - Y - 4) % m

    # All monotone paths in the full rectangle.
    total = (rect_sum(W, H) - (W + 1) * (H + 1)) % m

    # Paths starting inside the forbidden rectangle.
    A = W - R
    B = W - L
    Cb = H - U
    Db = H - D
    T = (
        rect_sum(B, Db)
        - rect_sum(A - 1, Db)
        - rect_sum(B, Cb - 1)
        + rect_sum(A - 1, Cb - 1)
    ) % m
    area = (R - L + 1) * (U - D + 1) % m
    inside = (T - area) % m

    # Invalid paths starting outside and first entering from the left side.
    left = 0
    if L > 0:
        fct = fact
        invf = invfact
        length = U - D + 1

        # y = D..U
        # C(L+y+1, L) - 1
        # C(W-L+H-y+2, W-L+1) - 1
        n1 = L + D + 1
        n2 = W - L + H - D + 2
        i1 = D + 1
        i2 = H - D + 1

        invL = invf[L]
        invM = invf[W - L + 1]

        for _ in range(length):
            c1 = (fct[n1] * invL * invf[i1]) % m - 1
            c2 = (fct[n2] * invM * invf[i2]) % m - 1
            left += c1 * c2
            n1 += 1
            n2 -= 1
            i1 += 1
            i2 -= 1
        left %= m

    # Invalid paths starting outside and first entering from the bottom side.
    bottom = 0
    if D > 0:
        fct = fact
        invf = invfact
        length = R - L + 1

        # x = L..R
        # C(x+D+1, D) - 1
        # C(W-x+H-D+2, H-D+1) - 1
        n1 = L + D + 1
        n2 = W - L + H - D + 2
        i1 = L + 1
        i2 = W - L + 1

        invD = invf[D]
        invHD = invf[H - D + 1]

        for _ in range(length):
            c1 = (fct[n1] * invD * invf[i1]) % m - 1
            c2 = (fct[n2] * invHD * invf[i2]) % m - 1
            bottom += c1 * c2
            n1 += 1
            n2 -= 1
            i1 += 1
            i2 -= 1
        bottom %= m

    ans = (total - inside - left - bottom) % m
    print(ans)

if __name__ == "__main__":
    main()