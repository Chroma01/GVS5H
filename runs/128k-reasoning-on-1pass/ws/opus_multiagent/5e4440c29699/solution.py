import sys
import math

MOD = 998244353


def _cumprod_mod(np, a):
    n = a.size
    if n == 0:
        return a
    b = int(math.isqrt(n)) + 1
    rows = (n + b - 1) // b
    pad = rows * b - n
    if pad:
        a = np.concatenate([a, np.ones(pad, dtype=np.int64)])
    m = a.reshape(rows, b).copy()
    for j in range(1, b):
        m[:, j] = m[:, j] * m[:, j - 1] % MOD
    ends = m[:, -1].tolist()
    pref = np.empty(rows, dtype=np.int64)
    cur = 1
    for i in range(rows):
        pref[i] = cur
        cur = cur * ends[i] % MOD
    m *= pref[:, None]
    m %= MOD
    return m.reshape(-1)[:n]


def _build_np(np, N):
    arr = np.arange(N + 1, dtype=np.int64)
    arr[0] = 1
    fact = _cumprod_mod(np, arr)
    del arr
    invN = pow(int(fact[N]), MOD - 2, MOD)
    invfact = np.empty(N + 1, dtype=np.int64)
    invfact[N] = invN
    if N > 0:
        rev = np.arange(N, 0, -1, dtype=np.int64)
        c = _cumprod_mod(np, rev)
        del rev
        invfact[:N] = invN * c[::-1] % MOD
        del c
    return fact, invfact


def main():
    data = sys.stdin.buffer.read().split()
    W, H, L, R, D, U = (int(v) for v in data[:6])

    N = W + H + 10

    try:
        import numpy as np
    except Exception:
        np = None

    if np is not None:
        fl, ifl = _build_np(np, N)
    else:
        fl = [1] * (N + 1)
        f = 1
        for i in range(1, N + 1):
            f = f * i % MOD
            fl[i] = f
        ifl = [1] * (N + 1)
        ifl[N] = pow(fl[N], MOD - 2, MOD)
        for i in range(N, 0, -1):
            ifl[i - 1] = ifl[i] * i % MOD

    def g(m, n):
        # sum_{i<=m, j<=n} C(i+j,i) = C(m+n+2, m+1) - 1
        if m < 0 or n < 0:
            return 0
        return (int(fl[m + n + 2]) * int(ifl[m + 1]) % MOD * int(ifl[n + 1]) % MOD - 1) % MOD

    def rectC(i0, i1, j0, j1):
        if i0 > i1 or j0 > j1:
            return 0
        return (g(i1, j1) - g(i0 - 1, j1) - g(i1, j0 - 1) + g(i0 - 1, j0 - 1)) % MOD

    def sum_g(a0, a1, b0, b1):
        # sum_{a=a0..a1, b=b0..b1} g(a,b)
        if a0 > a1 or b0 > b1:
            return 0
        return (rectC(a0 + 1, a1 + 1, b0 + 1, b1 + 1) - (a1 - a0 + 1) * (b1 - b0 + 1)) % MOD

    Tfull = sum_g(0, W, 0, H)
    Shole = sum_g(W - R, W - L, H - U, H - D)
    Thole = sum_g(L, R, D, U)
    Tboth = sum_g(0, R - L, 0, U - D)

    S1 = (Tfull - Shole - Thole + Tboth) % MOD

    S2 = 0

    if np is not None:
        def gv(m, n):
            # vectorized g, assumes all args >= 0
            idx = m + n + 2
            return (fl[idx] * ifl[m + 1] % MOD * ifl[n + 1] % MOD - 1) % MOD

        if L >= 1:
            y = np.arange(D, U + 1, dtype=np.int64)
            A = gv(L - 1, y)
            Bt = (gv(W - L, H - y) - gv(R - L, U - y)) % MOD
            S2 = (S2 + int((A * Bt % MOD).sum() % MOD)) % MOD
            del y, A, Bt

        if D >= 1:
            x = np.arange(L, R + 1, dtype=np.int64)
            A = gv(x, D - 1)
            Bt = (gv(W - x, H - D) - gv(R - x, U - D)) % MOD
            S2 = (S2 + int((A * Bt % MOD).sum() % MOD)) % MOD
            del x, A, Bt
    else:
        if L >= 1:
            t = 0
            for y in range(D, U + 1):
                t += g(L - 1, y) * ((g(W - L, H - y) - g(R - L, U - y)) % MOD) % MOD
            S2 = (S2 + t) % MOD
        if D >= 1:
            t = 0
            for x in range(L, R + 1):
                t += g(x, D - 1) * ((g(W - x, H - D) - g(R - x, U - D)) % MOD) % MOD
            S2 = (S2 + t) % MOD

    ans = (S1 - S2) % MOD
    sys.stdout.write(str(ans % MOD) + "\n")


main()