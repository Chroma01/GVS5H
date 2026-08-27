import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    W, H, L, R, D, U = map(int, data)

    mod = MOD
    N = W + H + 5

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % mod

    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], mod - 2, mod)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % mod

    f = fact
    inv = invfact
    mm = mod

    # Total number of monotone paths in the full rectangle.
    full = (f[W + H + 4] * inv[H + 2] * inv[W + 2]) % mm
    full -= W + H + 4
    full -= (W + 1) * (H + 1)

    # Prefix sum of C(a+b+2, b+1) for 0 <= a <= A, 0 <= b <= B.
    def T(A, B):
        if A < 0 or B < 0:
            return 0
        return (f[A + B + 4] * inv[B + 2] * inv[A + 2]) % mm - A - B - 4

    # Paths that start inside the forbidden rectangle.
    a0 = W - R
    a1 = W - L
    b0 = H - U
    b1 = H - D
    area = (a1 - a0 + 1) * (b1 - b0 + 1)
    start_inside = (
        T(a1, b1)
        - T(a0 - 1, b1)
        - T(a1, b0 - 1)
        + T(a0 - 1, b0 - 1)
        - area
    )

    # Paths whose first forbidden point is entered from the left side.
    left_entry = 0
    if L > 0:
        invL = inv[L]
        invwL1 = inv[W - L + 1]
        bp = L + 1
        bq = W - L + H + 2
        H1 = H + 1
        s = 0
        for y in range(D, U + 1):
            p = (f[bp + y] * invL * inv[y + 1]) % mm - 1
            q = (f[bq - y] * invwL1 * inv[H1 - y]) % mm - 1
            s += p * q
        left_entry = s

    # Paths whose first forbidden point is entered from the bottom side.
    bottom_entry = 0
    if D > 0:
        invD = inv[D]
        invhD1 = inv[H - D + 1]
        bp = D + 1
        bq = W + H - D + 2
        W1 = W + 1
        s = 0
        for x in range(L, R + 1):
            p = (f[bp + x] * inv[x + 1] * invD) % mm - 1
            q = (f[bq - x] * inv[W1 - x] * invhD1) % mm - 1
            s += p * q
        bottom_entry = s

    ans = (full - start_inside - left_entry - bottom_entry) % mod
    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    main()