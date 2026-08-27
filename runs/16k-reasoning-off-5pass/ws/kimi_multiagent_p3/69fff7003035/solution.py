import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    mod = MOD

    # Group numbers 1..N by digit length: (d, m_d, S_d)
    groups = []
    d = 1
    while True:
        lo = 10 ** (d - 1)
        if lo > N:
            break
        hi = min(10 ** d - 1, N)
        m = hi - lo + 1
        s = (lo + hi) * m // 2 % mod
        groups.append((d, m, s))
        d += 1

    # Factorials / inverse factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % mod
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], mod - 2, mod)
    for i in range(N, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % mod

    def comb(n, k):
        return fact[n] * inv_fact[k] % mod * inv_fact[n - k] % mod

    # Factor polynomials F_d(x) = (1 + 10^d x)^{m_d}
    factors = []
    for (dd, m, s) in groups:
        a = pow(10, dd, mod)
        poly = [1] * (m + 1)
        aj = 1
        for j in range(1, m + 1):
            aj = aj * a % mod
            poly[j] = comb(m, j) * aj % mod
        factors.append(poly)

    # ---------------- convolution backend ----------------
    conv = None
    try:
        import numpy as np

        def conv_numpy(a, b):
            n = len(a) + len(b) - 1
            L = 1 << (n - 1).bit_length()
            mask = (1 << 15) - 1
            aa = np.array(a, dtype=np.int64)
            bb = np.array(b, dtype=np.int64)
            a0 = aa & mask
            a1 = aa >> 15
            b0 = bb & mask
            b1 = bb >> 15
            fa0 = np.fft.rfft(a0, L)
            fa1 = np.fft.rfft(a1, L)
            fb0 = np.fft.rfft(b0, L)
            fb1 = np.fft.rfft(b1, L)
            c00 = np.rint(np.fft.irfft(fa0 * fb0, L)[:n]).astype(np.int64) % mod
            c01 = np.rint(np.fft.irfft(fa0 * fb1 + fa1 * fb0, L)[:n]).astype(np.int64) % mod
            c11 = np.rint(np.fft.irfft(fa1 * fb1, L)[:n]).astype(np.int64) % mod
            c = (c00 + (c01 << 15) + (c11 << 30)) % mod
            return c.tolist()

        conv = conv_numpy
    except Exception:
        G_ROOT = 3
        _ntt_cache = {}

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
                key = (length, invert)
                roots = _ntt_cache.get(key)
                if roots is None:
                    wlen = pow(G_ROOT, (mod - 1) // length, mod)
                    if invert:
                        wlen = pow(wlen, mod - 2, mod)
                    half = length >> 1
                    roots = [1] * half
                    for t in range(1, half):
                        roots[t] = roots[t - 1] * wlen % mod
                    _ntt_cache[key] = roots
                half = length >> 1
                for i in range(0, n, length):
                    k = i
                    for w in roots:
                        u = a[k]
                        v = a[k + half] * w % mod
                        s1 = u + v
                        if s1 >= mod:
                            s1 -= mod
                        a[k] = s1
                        s2 = u - v
                        if s2 < 0:
                            s2 += mod
                        a[k + half] = s2
                        k += 1
                length <<= 1
            if invert:
                inv_n = pow(n, mod - 2, mod)
                for i in range(n):
                    a[i] = a[i] * inv_n % mod

        def conv_ntt(a, b):
            n = len(a) + len(b) - 1
            L = 1 << (n - 1).bit_length()
            fa = a + [0] * (L - len(a))
            fb = b + [0] * (L - len(b))
            ntt(fa, False)
            ntt(fb, False)
            for i in range(L):
                fa[i] = fa[i] * fb[i] % mod
            ntt(fa, True)
            return fa[:n]

        conv = conv_ntt

    def conv_naive(a, b):
        res = [0] * (len(a) + len(b) - 1)
        for i, ai in enumerate(a):
            if ai:
                ri = i
                for j, bj in enumerate(b):
                    if bj:
                        res[ri + j] = (res[ri + j] + ai * bj) % mod
        return res

    # Multiply all factors, pairing smallest first (Huffman-style)
    import heapq
    heap = [(len(p), i, p) for i, p in enumerate(factors)]
    heapq.heapify(heap)
    uid = len(factors)
    while len(heap) > 1:
        _, _, p1 = heapq.heappop(heap)
        _, _, p2 = heapq.heappop(heap)
        if len(p1) * len(p2) <= 4096:
            p = conv_naive(p1, p2)
        else:
            p = conv(p1, p2)
        heapq.heappush(heap, (len(p), uid, p))
        uid += 1
    P = heap[0][2]  # e_0..e_N

    # Weights w_k = k! (N-1-k)!
    w = [fact[k] * fact[N - 1 - k] % mod for k in range(N)]

    # For each digit group: q = P / (1 + 10^d x); G = sum w_k q_k; ans += S_d * G
    answer = 0
    for (dd, m, s) in groups:
        a = pow(10, dd, mod)
        Gv = 0
        q = 0
        for k in range(N):
            q = (P[k] - a * q) % mod
            Gv = (Gv + w[k] * q) % mod
        answer = (answer + s * Gv) % mod

    print(answer)

main()