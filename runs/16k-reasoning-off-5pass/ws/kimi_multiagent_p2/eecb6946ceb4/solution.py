import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = list(map(int, data[1:1 + n]))
    V = max(S)

    try:
        import numpy as np
        size = 1
        while size < 2 * V + 1:
            size <<= 1
        f = np.zeros(size, dtype=np.float64)
        f[np.array(S, dtype=np.int64)] = 1.0
        F = np.fft.rfft(f)
        conv = np.rint(np.fft.irfft(F * F, size)).astype(np.int64)
        idx = np.array(S, dtype=np.int64) * 2
        ans = int(((conv[idx] - 1) // 2).sum())
        print(ans)
        return
    except ImportError:
        pass

    # Fallback: pure-Python NTT modulo 998244353 (coefficients <= 1e6 < mod)
    MOD = 998244353
    G = 3

    def ntt(a, invert):
        m = len(a)
        j = 0
        for i in range(1, m):
            bit = m >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j |= bit
            if i < j:
                a[i], a[j] = a[j], a[i]
        length = 2
        while length <= m:
            wlen = pow(G, (MOD - 1) // length, MOD)
            if invert:
                wlen = pow(wlen, MOD - 2, MOD)
            half = length >> 1
            for i in range(0, m, length):
                w = 1
                for k in range(i, i + half):
                    u = a[k]
                    v = a[k + half] * w % MOD
                    a[k] = u + v if u + v < MOD else u + v - MOD
                    a[k + half] = u - v if u >= v else u - v + MOD
                    w = w * wlen % MOD
            length <<= 1
        if invert:
            inv = pow(m, MOD - 2, MOD)
            for i in range(m):
                a[i] = a[i] * inv % MOD

    size = 1
    while size < 2 * V + 1:
        size <<= 1
    fa = [0] * size
    for x in S:
        fa[x] = 1
    ntt(fa, False)
    for i in range(size):
        fa[i] = fa[i] * fa[i] % MOD
    ntt(fa, True)
    ans = 0
    for b in S:
        ans += (fa[2 * b] - 1) // 2
    print(ans)

solve()