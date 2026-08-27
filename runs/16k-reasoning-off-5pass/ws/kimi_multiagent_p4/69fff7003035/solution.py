import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    N = int(data[0])

    # ---- classify 1..N by digit length ----
    maxd = len(str(N))
    cnt = [0] * (maxd + 1)      # cnt[c] = number of values with c digits
    valsum = [0] * (maxd + 1)   # sum of values with c digits (mod MOD)
    q = [0] * (maxd + 1)        # q[c] = 10^c mod MOD
    pw = 1 % MOD
    for c in range(1, maxd + 1):
        pw = pw * 10 % MOD
        q[c] = pw

    lo = 1
    for c in range(1, maxd + 1):
        hi = min(N, 10 ** c - 1)
        if lo > hi:
            break
        n_c = hi - lo + 1
        cnt[c] = n_c
        # sum of arithmetic series lo..hi, halve the even factor before mod
        if n_c % 2 == 0:
            s = (lo + hi) % MOD * ((n_c // 2) % MOD) % MOD
        else:
            s = ((lo + hi) // 2) % MOD * (n_c % MOD) % MOD
        valsum[c] = s % MOD
        lo = 10 ** c

    # ---- factorials / inverse factorials ----
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def comb(n, k):
        if k < 0 or k > n:
            return 0
        return fact[n] * invfact[k] % MOD * invfact[n - k] % MOD

    # ---- class polynomials F_c[k] = C(n_c,k) * q_c^k ----
    polys = []
    for c in range(1, maxd + 1):
        n_c = cnt[c]
        if n_c == 0:
            continue
        f = [0] * (n_c + 1)
        qc = q[c]
        qp = 1
        for k in range(n_c + 1):
            f[k] = comb(n_c, k) * qp % MOD
            qp = qp * qc % MOD
        polys.append(f)

    def naive_mul(a, b):
        res = [0] * (len(a) + len(b) - 1)
        for i, ai in enumerate(a):
            if ai == 0:
                continue
            ri = i
            for j, bj in enumerate(b):
                res[ri + j] = (res[ri + j] + ai * bj) % MOD
        return res

    try:
        import numpy as np
        HAVE_NP = True
    except Exception:
        HAVE_NP = False

    if HAVE_NP:
        # Precompute bit-reversal permutations per size (cache)
        _rev_cache = {}

        def bitrev_perm(n):
            r = _rev_cache.get(n)
            if r is None:
                L = n.bit_length() - 1
                rev = [0] * n
                for i in range(1, n):
                    rev[i] = (rev[i >> 1] >> 1) | ((i & 1) << (L - 1))
                r = np.array(rev, dtype=np.int64)
                _rev_cache[n] = r
            return r

        def ntt(a, invert):
            # a: np.int64 array, length = power of two, values in [0, MOD)
            n = a.shape[0]
            a = a[bitrev_perm(n)]
            length = 2
            while length <= n:
                half = length >> 1
                wlen = pow(3, (MOD - 1) // length, MOD)
                if invert:
                    wlen = pow(wlen, MOD - 2, MOD)
                tw = np.empty(half, dtype=np.int64)
                w = 1
                for i in range(half):
                    tw[i] = w
                    w = w * wlen % MOD
                a = a.reshape(-1, length)
                left = a[:, :half].copy()          # copy: avoid overwriting before second use
                right = a[:, half:] * tw % MOD     # fresh array
                a[:, :half] = (left + right) % MOD
                a[:, half:] = (left - right) % MOD
                a = a.reshape(-1)
                length <<= 1
            if invert:
                inv_n = pow(n, MOD - 2, MOD)
                a = a * inv_n % MOD
            return a

        def ntt_mul(a, b):
            need = len(a) + len(b) - 1
            n = 1
            while n < need:
                n <<= 1
            fa = np.zeros(n, dtype=np.int64)
            fb = np.zeros(n, dtype=np.int64)
            fa[:len(a)] = a
            fb[:len(b)] = b
            fa = ntt(fa, False)
            fb = ntt(fb, False)
            fa = fa * fb % MOD
            fa = ntt(fa, True)
            return [int(x) for x in fa[:need]]

        def mul(a, b):
            if len(a) * len(b) <= 4096:
                return naive_mul(a, b)
            return ntt_mul(a, b)
    else:
        def mul(a, b):
            return naive_mul(a, b)

    # ---- product tree ----
    while len(polys) > 1:
        nxt = []
        for i in range(0, len(polys), 2):
            if i + 1 < len(polys):
                nxt.append(mul(polys[i], polys[i + 1]))
            else:
                nxt.append(polys[i])
        polys = nxt
    P = polys[0] if polys else [1]
    # P has degree N (length N+1)

    # ---- w[k] = k! (N-1-k)! ----
    w = [0] * N
    for k in range(N):
        w[k] = fact[k] * fact[N - 1 - k] % MOD

    # ---- per class: Q = P / (1 + q_c x); H_c = sum Q[k] w[k] ----
    ans = 0
    for c in range(1, maxd + 1):
        if cnt[c] == 0:
            continue
        qc = q[c]
        H = 0
        qkm1 = 0  # Q[k-1]
        for k in range(N):
            Qk = (P[k] - qc * qkm1) % MOD
            H = (H + Qk * w[k]) % MOD
            qkm1 = Qk
        ans = (ans + valsum[c] * H) % MOD

    print(ans % MOD)

main()