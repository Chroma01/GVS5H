import sys

MOD = 998244353


def solve(N: int) -> int:
    mod = MOD

    # ---- digit-length groups ----
    groups = []  # (L, count, sum_of_values mod p)
    lo = 1
    L = 1
    while lo <= N:
        hi = min(10**L - 1, N)
        c = hi - lo + 1
        s = (lo + hi) * c // 2 % mod
        groups.append((L, c, s))
        lo = hi + 1
        L += 1

    # ---- factorials ----
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % mod
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], mod - 2, mod)
    for i in range(N, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % mod

    # ---- per-group polynomials (1 + a y)^c, coefficients C(c,k) a^k ----
    polys = []
    for (L, c, _) in groups:
        a = pow(10, L, mod)
        g = [0] * (c + 1)
        ak = 1
        for k in range(c + 1):
            g[k] = fact[c] * inv_fact[k] % mod * inv_fact[c - k] % mod * ak % mod
            ak = ak * a % mod
        polys.append(g)

    # ---- product P(y) of all group polynomials ----
    try:
        import numpy as np

        def convolution(a, b):
            la, lb = len(a), len(b)
            if la == 0 or lb == 0:
                return []
            if min(la, lb) <= 32:
                res = [0] * (la + lb - 1)
                for i, ai in enumerate(a):
                    if ai:
                        for j, bj in enumerate(b):
                            res[i + j] = (res[i + j] + ai * bj) % mod
                return res
            n = 1 << (la + lb - 2).bit_length()
            B = 1 << 15
            a = np.array(a, dtype=np.int64)
            b = np.array(b, dtype=np.int64)
            a0 = a % B
            a1 = a >> 15
            b0 = b % B
            b1 = b >> 15
            fa0 = np.fft.rfft(a0, n)
            fb0 = np.fft.rfft(b0, n)
            fa1 = np.fft.rfft(a1, n)
            fb1 = np.fft.rfft(b1, n)
            c0 = np.rint(np.fft.irfft(fa0 * fb0, n)[: la + lb - 1]).astype(np.int64)
            c1 = np.rint(
                np.fft.irfft(fa0 * fb1 + fa1 * fb0, n)[: la + lb - 1]
            ).astype(np.int64)
            c2 = np.rint(np.fft.irfft(fa1 * fb1, n)[: la + lb - 1]).astype(np.int64)
            res = (c0 + ((c1 % mod) << 15) + ((c2 % mod) << 30)) % mod
            return res.tolist()

        P = [1]
        for g in polys:
            P = convolution(P, g)
    except ImportError:
        # ---- pure-Python NTT fallback ----
        def ntt(a, invert):
            n = len(a)
            j = 0
            for i in range(1, n):
                bit = n >> 1
                while j & bit:
                    j ^= bit
                    bit >>= 1
                j |= bit
                if i < j:
                    a[i], a[j] = a[j], a[i]
            length = 2
            while length <= n:
                wlen = pow(3, (mod - 1) // length, mod)
                if invert:
                    wlen = pow(wlen, mod - 2, mod)
                half = length >> 1
                for i in range(0, n, length):
                    w = 1
                    for k in range(i, i + half):
                        u = a[k]
                        v = a[k + half] * w % mod
                        a[k] = u + v if u + v < mod else u + v - mod
                        a[k + half] = u - v if u >= v else u - v + mod
                        w = w * wlen % mod
                length <<= 1
            if invert:
                inv_n = pow(n, mod - 2, mod)
                for i in range(n):
                    a[i] = a[i] * inv_n % mod

        def convolution_ntt(a, b):
            need = len(a) + len(b) - 1
            n = 1 << (need - 1).bit_length()
            fa = a + [0] * (n - len(a))
            fb = b + [0] * (n - len(b))
            ntt(fa, False)
            ntt(fb, False)
            for i in range(n):
                fa[i] = fa[i] * fb[i] % mod
            ntt(fa, True)
            return fa[:need]

        P = [1]
        for g in polys:
            P = convolution_ntt(P, g)

    # ---- per-group excluded polynomial, weight, accumulate answer ----
    ans = 0
    for (L, c, s) in groups:
        a = pow(10, L, mod)
        prev = 0
        W = 0
        for m in range(N):
            prev = (P[m] - a * prev) % mod
            W = (W + fact[m] * fact[N - 1 - m] % mod * prev) % mod
        ans = (ans + s * W) % mod
    return ans


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    print(solve(N) % MOD)


if __name__ == "__main__":
    main()