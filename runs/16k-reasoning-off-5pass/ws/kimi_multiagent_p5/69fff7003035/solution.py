import sys

MOD = 998244353
G = 3  # primitive root of MOD


# ------------------------- pure python NTT (fallback) -------------------------
def _ntt(a, invert):
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
    mod = MOD
    while length <= n:
        wlen = pow(G, (mod - 1) // length, mod)
        if invert:
            wlen = pow(wlen, mod - 2, mod)
        half = length >> 1
        for i in range(0, n, length):
            w = 1
            ii = i + half
            for jj in range(i, ii):
                u = a[jj]
                v = a[jj + half] * w % mod
                s = u + v
                if s >= mod:
                    s -= mod
                a[jj] = s
                d = u - v
                if d < 0:
                    d += mod
                a[jj + half] = d
                w = w * wlen % mod
        length <<= 1
    if invert:
        inv_n = pow(n, mod - 2, mod)
        for i in range(n):
            a[i] = a[i] * inv_n % mod
    return a


def _convolve_ntt(a, b):
    n = len(a) + len(b) - 1
    size = 1 << (n - 1).bit_length()
    fa = a + [0] * (size - len(a))
    fb = b + [0] * (size - len(b))
    _ntt(fa, False)
    _ntt(fb, False)
    for i in range(size):
        fa[i] = fa[i] * fb[i] % MOD
    _ntt(fa, True)
    return fa[:n]


# ------------------------- numpy FFT convolution (primary) -------------------------
def _make_convolve_numpy():
    import numpy as np

    def convolve(a, b):
        n = len(a) + len(b) - 1
        size = 1 << (n - 1).bit_length()
        mask = (1 << 15) - 1
        a0 = np.array([x & mask for x in a], dtype=np.float64)
        a1 = np.array([x >> 15 for x in a], dtype=np.float64)
        b0 = np.array([x & mask for x in b], dtype=np.float64)
        b1 = np.array([x >> 15 for x in b], dtype=np.float64)

        fa0 = np.fft.fft(a0, size)
        fa1 = np.fft.fft(a1, size)
        fb0 = np.fft.fft(b0, size)
        fb1 = np.fft.fft(b1, size)

        c00 = np.rint(np.fft.ifft(fa0 * fb0).real[:n]).astype(np.int64)
        c01 = np.rint(np.fft.ifft(fa0 * fb1).real[:n]).astype(np.int64)
        c10 = np.rint(np.fft.ifft(fa1 * fb0).real[:n]).astype(np.int64)
        c11 = np.rint(np.fft.ifft(fa1 * fb1).real[:n]).astype(np.int64)

        res = (c00 % MOD
               + ((c01 + c10) % MOD) * (1 << 15)
               + (c11 % MOD) * (1 << 30)) % MOD
        return res.tolist()

    return convolve


try:
    _convolve = _make_convolve_numpy()
except Exception:
    _convolve = _convolve_ntt


def solve(N):
    # factorials / inverse factorials up to N
    fac = [1] * (N + 1)
    for i in range(1, N + 1):
        fac[i] = fac[i - 1] * i % MOD
    ifac = [1] * (N + 1)
    ifac[N] = pow(fac[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        ifac[i - 1] = ifac[i] * i % MOD

    def comb(n, k):
        if k < 0 or k > n:
            return 0
        return fac[n] * ifac[k] % MOD * ifac[n - k] % MOD

    # digit-length groups for numbers 1..N
    maxd = len(str(N))
    cnt = [0] * (maxd + 1)
    ssum = [0] * (maxd + 1)
    lo = 1
    for k in range(1, maxd + 1):
        hi = min(N, 10 ** k - 1)
        c = hi - lo + 1
        cnt[k] = c
        ssum[k] = (lo + hi) * c // 2 % MOD
        lo = hi + 1

    # a_k = 10^k mod MOD, w_k = -a_k mod MOD
    a = [0] * (maxd + 1)
    w = [0] * (maxd + 1)
    for k in range(1, maxd + 1):
        a[k] = pow(10, k, MOD)
        w[k] = (MOD - a[k]) % MOD

    # e_t: elementary symmetric sums of {a_v}, via product of (1 + a_k y)^cnt_k
    e = [1]
    for k in range(1, maxd + 1):
        c = cnt[k]
        if c == 0:
            continue
        poly = [0] * (c + 1)
        pw = 1
        ak = a[k]
        for s in range(c + 1):
            poly[s] = comb(c, s) * pw % MOD
            pw = pw * ak % MOD
        e = _convolve(e, poly)
        e = [x % MOD for x in e]
        if len(e) > N:  # only need e_0 .. e_{N-1}
            e = e[:N]

    # q_r = sum_k ssum_k * w_k^r, r = 0 .. N-1
    q = [0] * N
    for k in range(1, maxd + 1):
        if cnt[k] == 0:
            continue
        sk = ssum[k]
        if sk == 0:
            continue
        wk = w[k]
        pw = 1
        for r in range(N):
            q[r] = (q[r] + sk * pw) % MOD
            pw = pw * wk % MOD

    # h = e * q, need h_0 .. h_{N-1}
    h = _convolve(e, q)
    h = [x % MOD for x in h[:N]]

    # answer = sum_m m! (N-1-m)! h_m
    ans = 0
    for m in range(N):
        cm = fac[m] * fac[N - 1 - m] % MOD
        ans = (ans + cm * h[m]) % MOD

    return ans


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    print(solve(N))


main()