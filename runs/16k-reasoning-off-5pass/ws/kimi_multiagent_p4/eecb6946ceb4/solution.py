import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    S = list(map(int, data[1:1 + n]))
    if n < 3:
        print(0)
        return
    M = max(S)

    try:
        import numpy as np
        f = np.zeros(M + 1, dtype=np.float64)
        f[np.array(S, dtype=np.int64)] = 1.0
        size = 1
        while size < 2 * M + 1:
            size <<= 1
        F = np.fft.rfft(f, size)
        conv = np.fft.irfft(F * F, size)
        idx = 2 * np.array(S, dtype=np.int64)
        c = np.rint(conv[idx]).astype(np.int64)
        ans = int(((c - 1) // 2).sum())
        print(ans)
    except ImportError:
        # Pure-Python NTT fallback, mod 998244353
        MOD = 998244353
        G = 3

        def modpow(a, e):
            r = 1
            a %= MOD
            while e:
                if e & 1:
                    r = r * a % MOD
                a = a * a % MOD
                e >>= 1
            return r

        def ntt(a, invert):
            n = len(a)
            j = 0
            for i in range(1, n):
                bit = n >> 1
                while j & bit:
                    j ^= bit
                    bit >>= 1
                j ^= bit
                if i < j:
                    a[i], a[j] = a[j], a[i]
            length = 2
            while length <= n:
                wlen = modpow(G, (MOD - 1) // length)
                if invert:
                    wlen = modpow(wlen, MOD - 2)
                half = length >> 1
                for i in range(0, n, length):
                    w = 1
                    for k in range(i, i + half):
                        u = a[k]
                        v = a[k + half] * w % MOD
                        a[k] = u + v if u + v < MOD else u + v - MOD
                        a[k + half] = u - v if u >= v else u - v + MOD
                        w = w * wlen % MOD
                length <<= 1
            if invert:
                inv_n = modpow(n, MOD - 2)
                for i in range(n):
                    a[i] = a[i] * inv_n % MOD

        size = 1
        while size < 2 * M + 1:
            size <<= 1
        fa = [0] * size
        for v in S:
            fa[v] = 1
        ntt(fa, False)
        for i in range(size):
            fa[i] = fa[i] * fa[i] % MOD
        ntt(fa, True)
        ans = 0
        for b in S:
            ans += (fa[2 * b] - 1) // 2
        print(ans)

solve()