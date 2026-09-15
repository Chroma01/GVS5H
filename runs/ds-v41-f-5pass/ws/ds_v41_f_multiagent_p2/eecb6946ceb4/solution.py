import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    S = list(map(int, data[1:1 + n]))
    del data

    maxv = max(S)
    target = 2 * maxv + 1
    L = 1
    while L < target:
        L <<= 1

    try:
        import numpy as np
        arr = np.array(S, dtype=np.int64)
        del S
        f = np.zeros(L, dtype=np.float64)
        f[arr] = 1.0
        F = np.fft.rfft(f)
        del f
        F *= F
        conv = np.fft.irfft(F, n=L)
        del F
        conv = np.rint(conv).astype(np.int64)
        ans = np.sum((conv[2 * arr] - 1) // 2)
        print(int(ans))
        return
    except ImportError:
        pass

    MOD = 998244353
    G = 3
    f = [0] * L
    for x in S:
        f[x] = 1

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
            wlen = pow(G, (MOD - 1) // length, MOD)
            if invert:
                wlen = pow(wlen, MOD - 2, MOD)
            half = length >> 1
            for i in range(0, n, length):
                w = 1
                for j in range(i, i + half):
                    u = a[j]
                    v = a[j + half] * w % MOD
                    x = u + v
                    if x >= MOD:
                        x -= MOD
                    y = u - v
                    if y < 0:
                        y += MOD
                    a[j] = x
                    a[j + half] = y
                    w = w * wlen % MOD
            length <<= 1
        if invert:
            inv_n = pow(n, MOD - 2, MOD)
            for i in range(n):
                a[i] = a[i] * inv_n % MOD

    ntt(f, False)
    for i in range(L):
        f[i] = f[i] * f[i] % MOD
    ntt(f, True)

    ans = 0
    for b in S:
        ans += (f[2 * b] - 1) // 2
    print(ans)

if __name__ == "__main__":
    main()