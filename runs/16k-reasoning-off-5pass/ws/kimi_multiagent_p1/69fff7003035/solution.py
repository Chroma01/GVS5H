import sys


def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    p = MOD

    # factorials / inverse factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % p
    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], p - 2, p)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % p

    # digit-length groups: numbers in [1..N] with d digits
    cs, sigmas, ws = [], [], []
    d = 1
    while 10 ** (d - 1) <= N:
        lo = 10 ** (d - 1)
        hi = min(10 ** d - 1, N)
        c = hi - lo + 1
        cs.append(c)
        sigmas.append((lo + hi) * c // 2 % p)
        ws.append(pow(10, d, p))
        d += 1

    # convolution mod p via numpy split-FFT (base 2^15), with naive fallback
    try:
        import numpy as np

        def conv(a, b):
            n = len(a) + len(b) - 1
            sz = 1 << (n - 1).bit_length()
            B = 1 << 15
            mask = B - 1
            aa = np.asarray(a, dtype=np.int64)
            bb = np.asarray(b, dtype=np.int64)
            a0 = (aa & mask).astype(np.float64)
            a1 = (aa >> 15).astype(np.float64)
            b0 = (bb & mask).astype(np.float64)
            b1 = (bb >> 15).astype(np.float64)
            A0 = np.fft.rfft(a0, sz)
            A1 = np.fft.rfft(a1, sz)
            B0 = np.fft.rfft(b0, sz)
            B1 = np.fft.rfft(b1, sz)
            c00 = np.rint(np.fft.irfft(A0 * B0, sz)[:n]).astype(np.int64)
            c01 = np.rint(np.fft.irfft(A0 * B1 + A1 * B0, sz)[:n]).astype(np.int64)
            c11 = np.rint(np.fft.irfft(A1 * B1, sz)[:n]).astype(np.int64)
            B2 = B * B % p
            res = (c00 % p + (c01 % p) * B + (c11 % p) * B2) % p
            return res.tolist()
    except ImportError:
        def conv(a, b):
            res = [0] * (len(a) + len(b) - 1)
            for i, ai in enumerate(a):
                if ai:
                    for j, bj in enumerate(b):
                        if bj:
                            res[i + j] = (res[i + j] + ai * bj) % p
            return res

    # H(z) = product over groups of (1 + w_d z)^{c_d}
    H = [1]
    for c, w in zip(cs, ws):
        fc = fact[c]
        P = [0] * (c + 1)
        wk = 1
        for k in range(c + 1):
            P[k] = fc * invfact[k] % p * invfact[c - k] % p * wk % p
            wk = wk * w % p
        H = conv(H, P)

    # fw[K] = K! * (N-1-K)!
    fw = [fact[K] * fact[N - 1 - K] % p for K in range(N)]

    # For each group d: G_d = H / (1 + w_d z), coefficients via g_K = h_K - w_d*g_{K-1}
    # term_d = sum_K fw[K] * G_d[K]; answer = sum_d sigma_d * term_d
    ans = 0
    h = H
    for sigma, w in zip(sigmas, ws):
        g = h[0]
        term = fw[0] * g % p
        for K in range(1, N):
            g = (h[K] - w * g) % p
            term = (term + fw[K] * g) % p
        ans = (ans + sigma * term) % p

    print(ans)


main()