import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = list(map(int, data[1:1 + n]))

    if n < 3:
        print(0)
        return

    max_v = max(S)

    try:
        import numpy as np
        # Indicator array of S
        f = np.zeros(max_v + 1, dtype=np.float64)
        f[np.array(S, dtype=np.int64)] = 1.0

        # Convolution size: need indices up to 2*max_v
        size = 1
        while size < 2 * max_v + 1:
            size <<= 1

        F = np.fft.rfft(f, size)
        conv = np.fft.irfft(F * F, size)

        # For each B in S: number of d>=1 with B-d, B+d in S
        # = (conv[2B] - 1) / 2  (subtract the (B,B) self-pair)
        idx = np.array(S, dtype=np.int64) * 2
        coeffs = np.rint(conv[idx]).astype(np.int64)
        ans = int(((coeffs - 1) // 2).sum())
        print(ans)
    except ImportError:
        # Fallback: pure-Python NTT (mod 998244353), exact arithmetic
        present = bytearray(max_v + 1)
        for v in S:
            present[v] = 1
        f = list(present)

        MOD = 998244353
        G = 3

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
                wlen = pow(G, (MOD - 1) // length, MOD)
                if invert:
                    wlen = pow(wlen, MOD - 2, MOD)
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
                inv_n = pow(n, MOD - 2, MOD)
                for i in range(n):
                    a[i] = a[i] * inv_n % MOD

        size = 1
        while size < 2 * max_v + 1:
            size <<= 1
        fa = f + [0] * (size - len(f))
        ntt(fa, False)
        for i in range(size):
            fa[i] = fa[i] * fa[i] % MOD
        ntt(fa, True)

        ans = 0
        for b in S:
            ans += (fa[2 * b] - 1) // 2
        print(ans)

main()