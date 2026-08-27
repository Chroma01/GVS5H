import sys
import numpy as np

def solve():
    data = sys.stdin.read().split()
    N = int(data[0]); P = int(data[1])
    E = N * (N - 1) // 2          # max edges
    U = N - 1                      # non-root vertices
    MASK = (1 << 15) - 1

    # ---------- binomials C(n,k) mod P ----------
    C = [[0] * (N + 1) for _ in range(N + 1)]
    for n in range(N + 1):
        C[n][0] = C[n][n] = 1 % P
        for k in range(1, n):
            C[n][k] = (C[n-1][k-1] + C[n-1][k]) % P

    # ---------- small exact convolutions (Python ints, then mod P) ----------
    def conv_exact(a, b):
        res = [0] * (len(a) + len(b) - 1)
        for i, ai in enumerate(a):
            if ai:
                for j, bj in enumerate(b):
                    if bj:
                        res[i + j] += ai * bj
        return res

    # A_a(x) = (1+x)^a - 1   (exact, coefficients are binomials)
    A = [None] * (N + 1)
    for a in range(N + 1):
        p = [1]
        for _ in range(a):
            p = conv_exact(p, [1, 1])
        p[0] -= 1
        A[a] = p

    # W_b(x) = (1+x)^{C(b,2)}  (exact)
    W = [None] * (N + 1)
    for b in range(N + 1):
        e = b * (b - 1) // 2
        p = [1]
        base = [1, 1]
        ee = e
        while ee:
            if ee & 1:
                p = conv_exact(p, base)
            ee >>= 1
            if ee:
                base = conv_exact(base, base)
        W[b] = p

    # ---------- kernels Q[a][b] = A_a^b * W_b  (mod P), cached split FFTs ----------
    Q = [[None] * (N + 1) for _ in range(N + 1)]
    kern_fft = [[dict() for _ in range(N + 1)] for _ in range(N + 1)]

    def build_kernel(a, b):
        q = Q[a][b]
        if q is None:
            pw = [1]
            Aa = A[a]
            for _ in range(b):
                pw = conv_exact(pw, Aa)
            qe = conv_exact(pw, W[b])
            q = np.array([v % P for v in qe], dtype=np.int64)
            Q[a][b] = q
        return q

    def get_kern_fft(a, b, n):
        d = kern_fft[a][b]
        hit = d.get(n)
        if hit is not None:
            return hit
        q = build_kernel(a, b)
        pad = np.zeros(n, dtype=np.int64)
        pad[:len(q)] = q
        lo = (pad & MASK).astype(np.float64)
        hi = (pad >> 15).astype(np.float64)
        out = (np.fft.rfft(lo, n), np.fft.rfft(hi, n))
        d[n] = out
        return out

    # ---------- DP table ----------
    # f[u][a][p] : dict d -> 1-D int64 numpy array (poly mod P)
    f = [[ [dict(), dict()] for _ in range(N + 1)] for _ in range(U + 1)]
    f[0][1][0][1] = np.ones(1, dtype=np.int64)   # L0 = {1}: u=0,a=1,p=0,d=1

    for u in range(0, U + 1):
        rem = U - u
        if rem == 0:
            break
        row_u = f[u]
        for a in range(1, N + 1):
            for p in (0, 1):
                dd = row_u[a][p]
                if not dd:
                    continue
                items = [(d, poly) for d, poly in dd.items()
                         if poly is not None and len(poly) > 0]
                if not items:
                    continue
                for b in range(1, rem + 1):
                    rows = []
                    tgts = []
                    maxlen = 0
                    rem2 = rem - b
                    for d, poly in items:
                        d2 = d - b if p == 0 else d + b
                        if d2 > rem2 or -d2 > rem2:
                            continue
                        rows.append(poly)
                        tgts.append(d2)
                        if len(poly) > maxlen:
                            maxlen = len(poly)
                    if not rows:
                        continue
                    kern = build_kernel(a, b)
                    lk = len(kern)
                    need = maxlen + lk - 1
                    n = 1
                    while n < need:
                        n <<= 1
                    Fk_lo, Fk_hi = get_kern_fft(a, b, n)

                    R = len(rows)
                    F = np.zeros((R, n), dtype=np.int64)
                    for r, poly in enumerate(rows):
                        F[r, :len(poly)] = poly
                    Flo = np.fft.rfft((F & MASK).astype(np.float64), n, axis=1)
                    Fhi = np.fft.rfft((F >> 15).astype(np.float64), n, axis=1)
                    c00 = np.fft.irfft(Flo * Fk_lo, n, axis=1)
                    c01 = np.fft.irfft(Flo * Fk_hi + Fhi * Fk_lo, n, axis=1)
                    c11 = np.fft.irfft(Fhi * Fk_hi, n, axis=1)
                    outlen = min(need, E + 1)
                    r00 = np.rint(c00[:, :outlen]).astype(np.int64)
                    r01 = np.rint(c01[:, :outlen]).astype(np.int64)
                    r11 = np.rint(c11[:, :outlen]).astype(np.int64)
                    conv_res = (r00 + (r01 << 15) + (r11 << 30)) % P

                    w = C[U - u][b]
                    if w != 1:
                        conv_res = (conv_res * w) % P

                    tgt_dict = f[u + b][b][p ^ 1]
                    for r in range(R):
                        d2 = tgts[r]
                        new = conv_res[r]
                        nz = np.nonzero(new)[0]
                        L = int(nz[-1]) + 1 if nz.size else 0
                        old = tgt_dict.get(d2)
                        if old is None:
                            if L:
                                tgt_dict[d2] = new[:L].copy()
                        else:
                            if L > len(old):
                                o = np.zeros(L, dtype=np.int64)
                                o[:len(old)] = old
                                old = o
                            old[:L] = (old[:L] + new[:L]) % P
                            tgt_dict[d2] = old

    ans = [0] * (E + 1)
    for a in range(1, N + 1):
        for p in (0, 1):
            poly = f[U][a][p].get(0)
            if poly is not None:
                for i, v in enumerate(poly):
                    ans[i] = (ans[i] + int(v)) % P

    sys.stdout.write(' '.join(str(ans[m] % P) for m in range(N - 1, E + 1)) + '\n')

solve()