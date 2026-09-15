import sys


def ntt(a, invert):
    mod = 998244353
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
        wlen = pow(3, (mod - 1) // length, mod)
        if invert:
            wlen = pow(wlen, mod - 2, mod)
        half = length >> 1
        roots = [1] * half
        for k in range(1, half):
            roots[k] = roots[k - 1] * wlen % mod
        for i in range(0, n, length):
            for k in range(half):
                u = a[i + k]
                v = a[i + k + half] * roots[k] % mod
                x = u + v
                if x >= mod:
                    x -= mod
                y = u - v
                if y < 0:
                    y += mod
                a[i + k] = x
                a[i + k + half] = y
        length <<= 1
    if invert:
        inv_n = pow(n, mod - 2, mod)
        for i in range(n):
            a[i] = a[i] * inv_n % mod


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    s = list(map(int, data[1:1 + n]))
    if n < 3:
        print(0)
        return

    try:
        import numpy as np
    except ImportError:
        np = None

    if np is not None:
        arr_s = np.array(s, dtype=np.int64)
        mx = int(arr_s.max())
        L = 1
        while L <= 2 * mx:
            L <<= 1
        arr = np.zeros(L, dtype=np.float64)
        arr[arr_s] = 1.0
        f = np.fft.rfft(arr)
        conv = np.fft.irfft(f * f, L)
        vals = np.rint(conv[2 * arr_s]).astype(np.int64)
        total = int(vals.sum())
        print((total - n) // 2)
        return

    # Pure-Python NTT fallback (modulus exceeds max coefficient, so exact).
    mx = max(s)
    L = 1
    while L <= 2 * mx:
        L <<= 1
    a = [0] * L
    for x in s:
        a[x] = 1
    ntt(a, False)
    mod = 998244353
    for i in range(L):
        a[i] = a[i] * a[i] % mod
    ntt(a, True)
    total = 0
    for x in s:
        total += a[2 * x]
    print((total - n) // 2)


main()