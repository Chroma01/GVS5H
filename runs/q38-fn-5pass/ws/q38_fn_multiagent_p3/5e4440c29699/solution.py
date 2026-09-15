import sys

MOD = 998244353


def left_range(lo, hi, L, W, H, f, ifa, mod, const1, const2):
    if lo > hi:
        return 0
    idx1 = L + lo + 1
    idx2 = W - L + H - lo + 2
    inv1 = lo + 1
    inv2 = H - lo + 1
    s = 0
    for _ in range(hi - lo + 1):
        c1 = (f[idx1] * const1 * ifa[inv1]) % mod
        c2 = (f[idx2] * const2 * ifa[inv2]) % mod
        s += (c1 - 1) * (c2 - 1)
        idx1 += 1
        idx2 -= 1
        inv1 += 1
        inv2 -= 1
    return s % mod


def bottom_range(lo, hi, W, H, D, f, ifa, mod, const1, const2):
    if lo > hi:
        return 0
    idx1 = lo + D + 1
    idx2 = W - lo + H - D + 2
    inv1 = lo + 1
    inv2 = W - lo + 1
    s = 0
    for _ in range(hi - lo + 1):
        c1 = (f[idx1] * const1 * ifa[inv1]) % mod
        c2 = (f[idx2] * const2 * ifa[inv2]) % mod
        s += (c1 - 1) * (c2 - 1)
        idx1 += 1
        idx2 -= 1
        inv1 += 1
        inv2 -= 1
    return s % mod


def main():
    W, H, L, R, D, U = map(int, sys.stdin.buffer.read().split())
    mod = MOD
    N = W + H + 4

    f = [1] * (N + 1)
    v = 1
    for i in range(1, N + 1):
        v = (v * i) % mod
        f[i] = v

    ifa = [1] * (N + 1)
    v = pow(f[N], mod - 2, mod)
    ifa[N] = v
    for i in range(N, 0, -1):
        v = (v * i) % mod
        ifa[i - 1] = v

    def C(n, k):
        if n < 0 or k < 0 or k > n:
            return 0
        return (f[n] * ifa[k] % mod) * ifa[n - k] % mod

    def T(n, m):
        if n < 0 or m < 0:
            return 0
        return (C(n + m + 4, n + 2) - n * m - 2 * n - 2 * m - 5) % mod

    ans = T(W, H)

    a0 = W - R
    a1 = W - L
    b0 = H - U
    b1 = H - D
    inside = (T(a1, b1) - T(a0 - 1, b1) - T(a1, b0 - 1) + T(a0 - 1, b0 - 1)) % mod
    ans = (ans - inside) % mod

    if L > 0:
        const1 = ifa[L]
        const2 = ifa[W - L + 1]
        length = U - D + 1
        comp_len = D + (H - U)
        if length <= comp_len:
            s_left = left_range(D, U, L, W, H, f, ifa, mod, const1, const2)
        else:
            full_left = (
                C(W + H + 4, H + 2)
                - C(W - L + H + 3, H + 2)
                - C(L - 1 + H + 3, H + 2)
            ) % mod
            sumc1 = (C(L - 1 + H + 3, L + 1) - 1) % mod
            sumc2 = (C(W - L + H + 3, W - L + 2) - 1) % mod
            full_left = (full_left - sumc1 - sumc2 + (H + 1)) % mod
            s_left = (
                full_left
                - left_range(0, D - 1, L, W, H, f, ifa, mod, const1, const2)
                - left_range(U + 1, H, L, W, H, f, ifa, mod, const1, const2)
            ) % mod
        ans -= s_left

    if D > 0:
        const1 = ifa[D]
        const2 = ifa[H - D + 1]
        length = R - L + 1
        comp_len = L + (W - R)
        if length <= comp_len:
            s_bottom = bottom_range(L, R, W, H, D, f, ifa, mod, const1, const2)
        else:
            full_bottom = (
                C(W + H + 4, W + 2)
                - C(H - D + W + 3, W + 2)
                - C(D + W + 2, W + 2)
            ) % mod
            sumc1 = (C(D + W + 2, W + 1) - 1) % mod
            sumc2 = (C(H - D + W + 3, W + 1) - 1) % mod
            full_bottom = (full_bottom - sumc1 - sumc2 + (W + 1)) % mod
            s_bottom = (
                full_bottom
                - bottom_range(0, L - 1, W, H, D, f, ifa, mod, const1, const2)
                - bottom_range(R + 1, W, W, H, D, f, ifa, mod, const1, const2)
            ) % mod
        ans -= s_bottom

    print(ans % mod)


if __name__ == "__main__":
    main()