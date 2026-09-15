import sys
import numpy as np

MOD = 998244353
MASK = (1 << 15) - 1
P15 = pow(2, 15, MOD)
P30 = pow(2, 30, MOD)


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].decode()
    M = 2 * N

    # necessary: vertex 1 must be black, vertex 2N must be white
    if S[0] != 'B' or S[-1] != 'W':
        sys.stdout.write("0\n")
        return

    Bp = [0] * (M + 1)
    Wp = [0] * (M + 1)
    b = w = 0
    for i in range(1, M + 1):
        if S[i - 1] == 'B':
            b += 1
        else:
            w += 1
        Bp[i] = b
        Wp[i] = w

    # ---------- reference O(N^2) DP (small inputs) ----------
    if M <= 800:
        f = [0] * (N + 1)
        f[0] = 1
        T = 0
        for i in range(1, M + 1):
            g = [0] * (N + 1)
            if S[i - 1] == 'B':
                for s in range(N + 1):
                    v = f[s]
                    if v:
                        ow = s + T
                        if ow >= 0:
                            g[s] = (g[s] + ow * v) % MOD
                        if s + 1 <= N:
                            g[s + 1] = (g[s + 1] + v) % MOD
                T -= 1
            else:
                for s in range(N + 1):
                    v = f[s]
                    if v:
                        g[s] = (g[s] + v) % MOD
                    if s + 1 <= N and f[s + 1]:
                        g[s] = (g[s] + (s + 1) * f[s + 1]) % MOD
                T += 1
            if i < M:
                g[0] = 0
            f = g
        sys.stdout.write(str(f[0] % MOD) + "\n")
        return

    # ---------- factorials ----------
    fact = [1] * (N + 2)
    for i in range(1, N + 2):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (N + 2)
    inv_fact[N + 1] = pow(fact[N + 1], MOD - 2, MOD)
    for i in range(N + 1, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # candidates: T_i = Wp[i]-Bp[i] >= 0 (positions >= 1, sorted by position)
    cand = [i for i in range(1, M + 1) if Wp[i] - Bp[i] >= 0]
    K = len(cand)
    Wc = [Wp[p] for p in cand]
    Bc = [Bp[p] for p in cand]
    Tc = [Wp[p] - Bp[p] for p in cand]

    h = [0] * K
    accum = [0] * K

    # ---------- NTT tables ----------
    need = 2 * N + 2
    max_L = 1
    while max_L < need:
        max_L <<= 1
    max_log = max_L.bit_length() - 1
    revs = [None] * (max_log + 1)
    fwd = [None] * (max_log + 1)
    invt = [None] * (max_log + 1)
    for k in range(1, max_log + 1):
        L = 1 << k
        idx = np.arange(L, dtype=np.uint32)
        rev = np.zeros(L, dtype=np.uint32)
        for bb in range(k):
            rev |= ((idx >> bb) & 1) << (k - 1 - bb)
        revs[k] = rev
        half = L >> 1
        wlen = pow(3, (MOD - 1) // L, MOD)
        pw = np.empty(half, dtype=np.int64)
        pw[0] = 1
        for x in range(1, half):
            pw[x] = pw[x - 1] * wlen % MOD
        fwd[k] = pw
        iw = pow(wlen, MOD - 2, MOD)
        ipw = np.empty(half, dtype=np.int64)
        ipw[0] = 1
        for x in range(1, half):
            ipw[x] = ipw[x - 1] * iw % MOD
        invt[k] = ipw

    def ntt(a, invert):
        L = a.shape[0]
        k = L.bit_length() - 1
        a[:] = a[revs[k]]
        length = 2
        level = 1
        while length <= L:
            half = length >> 1
            wv = invt[level] if invert else fwd[level]
            blk = a.reshape(-1, length)
            u = blk[:, :half].copy()
            v = blk[:, half:] * wv % MOD
            blk[:, :half] = (u + v) % MOD
            blk[:, half:] = (u - v) % MOD
            length <<= 1
            level += 1
        if invert:
            a[:] = a * pow(L, MOD - 2, MOD) % MOD

    def conv_ntt(A, F):
        n = len(A)
        m = len(F)
        L = 1
        while L < n + m - 1:
            L <<= 1
        a = np.zeros(L, dtype=np.int64)
        b2 = np.zeros(L, dtype=np.int64)
        a[:n] = A
        b2[:m] = F
        ntt(a, False)
        ntt(b2, False)
        a[:] = a * b2 % MOD
        ntt(a, True)
        return a[:n + m - 1]

    def conv_small_np(A, F):
        An = np.array(A, dtype=np.int64)
        Fn = np.array(F, dtype=np.int64)
        Ah = An >> 15
        Al = An & MASK
        Fh = Fn >> 15
        Fl = Fn & MASK
        c_ll = np.convolve(Al, Fl) % MOD
        c_lh = np.convolve(Al, Fh) % MOD
        c_hl = np.convolve(Ah, Fl) % MOD
        c_hh = np.convolve(Ah, Fh) % MOD
        res = (c_ll + ((c_lh + c_hl) % MOD) * P15 % MOD
               + (c_hh % MOD) * P30 % MOD) % MOD
        return res

    def conv(A, F):
        n = len(A)
        m = len(F)
        pr = n * m
        if pr <= 400:
            res = [0] * (n + m - 1)
            for i in range(n):
                ai = A[i]
                if ai:
                    for j2 in range(m):
                        res[i + j2] += ai * F[j2]
            return [x % MOD for x in res]
        if pr <= 250000:
            return conv_small_np(A, F)
        return conv_ntt(A, F)

    sys.setrecursionlimit(1 << 20)

    # CDQ over candidate indices
    def solve(a, r):
        if a == r:
            h[a] = (fact[Wc[a]] - accum[a]) % MOD * inv_fact[Tc[a]] % MOD
            return
        mid = (a + r) >> 1
        solve(a, mid)
        # merge left [a,mid] (sources) -> right [mid+1,r] (queries)
        items_b = []
        items_h = []
        for t in range(a, mid + 1):
            ht = h[t]
            if ht:
                items_b.append(Bc[t])
                items_h.append(ht)
        if items_b:
            bmin = items_b[0]
            bmax = items_b[-1]
            nA = bmax - bmin + 1
            olo = Wc[mid + 1] - bmin
            ohi = Wc[r] - bmin
            qlo = olo - (nA - 1)
            if qlo < 0:
                qlo = 0
            qhi = ohi
            if qhi >= qlo:
                A = [0] * nA
                for t in range(len(items_b)):
                    pos = items_b[t] - bmin
                    A[pos] = (A[pos] + items_h[t]) % MOD
                F = fact[qlo:qhi + 1]
                C = conv(A, F)
                lenC = len(C)
                for t in range(mid + 1, r + 1):
                    ci = Wc[t] - bmin - qlo
                    if 0 <= ci < lenC:
                        accum[t] = (accum[t] + int(C[ci])) % MOD
        solve(mid + 1, r)

    solve(0, K - 1)
    sys.stdout.write(str(h[K - 1] % MOD) + "\n")


main()