import sys
import numpy as np


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    P = int(data[1])
    D = N * (N - 1) // 2
    L = D + 1
    half = N // 2

    # Binomial coefficients mod P for n <= N
    C = [[0] * (N + 1) for _ in range(N + 1)]
    for n in range(N + 1):
        C[n][0] = 1 % P
        for k in range(1, n + 1):
            val = C[n - 1][k - 1]
            if k <= n - 1:
                val += C[n - 1][k]
            C[n][k] = val % P

    # bs[p, s, t] = ((1+t)^p - 1)^s * (1+t)^{C(s,2)} mod P
    bs = np.zeros((N + 1, N + 1, L), dtype=np.int64)
    for t in range(L):
        v = (1 + t) % P
        vp = [1] * (N + 1)
        for i in range(1, N + 1):
            vp[i] = vp[i - 1] * v % P
        for p in range(1, N + 1):
            term = (vp[p] - 1) % P
            cur = 1
            f2 = 1
            row = bs[p]
            for s in range(1, N + 1):
                cur = cur * term % P
                if s >= 2:
                    f2 = f2 * vp[s - 1] % P
                row[s, t] = cur * f2 % P

    # state: (used, odd_sum, prev_layer_size, last_layer_parity)
    dp = {(1, 0, 1, 0): np.ones(L, dtype=np.int64)}

    for u in range(1, N):
        keys = [k for k in dp if k[0] == u]
        if not keys:
            continue
        remaining = N - u
        cp = C[remaining]
        W = {}
        for p in range(1, N + 1):
            row = bs[p]
            Wp = [None] * (remaining + 1)
            for s in range(1, remaining + 1):
                Wp[s] = row[s] * cp[s] % P
            W[p] = Wp
        newadds = {}
        for key in keys:
            o = key[1]
            p = key[2]
            par = key[3]
            src = dp.pop(key)
            src %= P
            Wp = W[p]
            if par == 0:
                # next layer is odd-indexed: its vertices count toward o
                smax = half - o
                if smax > remaining:
                    smax = remaining
                for s in range(1, smax + 1):
                    tmp = src * Wp[s] % P
                    nk = (u + s, o + s, s, 1)
                    old = newadds.get(nk)
                    if old is None:
                        newadds[nk] = tmp
                    else:
                        old += tmp
            else:
                # next layer is even-indexed
                smax = half - (u - o)
                if smax > remaining:
                    smax = remaining
                for s in range(1, smax + 1):
                    tmp = src * Wp[s] % P
                    nk = (u + s, o, s, 0)
                    old = newadds.get(nk)
                    if old is None:
                        newadds[nk] = tmp
                    else:
                        old += tmp
        for k, v in newadds.items():
            old = dp.get(k)
            if old is None:
                dp[k] = v
            else:
                old += v

    total = np.zeros(L, dtype=np.int64)
    for (u, o, p, par), arr in dp.items():
        if u == N and o == half:
            total += arr % P
    total %= P
    y = [int(x) for x in total.tolist()]

    # Lagrange interpolation of the degree <= D polynomial through (t, y[t])
    Mp = [1]
    for t in range(L):
        new = [0] * (len(Mp) + 1)
        for i, c in enumerate(Mp):
            if c:
                new[i + 1] = (new[i + 1] + c) % P
                new[i] = (new[i] - c * t) % P
        Mp = new

    res = [0] * L
    for t in range(L):
        mp = 1
        for j in range(L):
            if j != t:
                mp = mp * (t - j) % P
        ct = y[t] * pow(mp, P - 2, P) % P
        if ct == 0:
            continue
        q = [0] * L
        q[L - 1] = Mp[L]
        for i in range(L - 1, 0, -1):
            q[i - 1] = (Mp[i] + t * q[i]) % P
        for i in range(L):
            res[i] = (res[i] + ct * q[i]) % P

    out = [str(res[M] % P) for M in range(N - 1, D + 1)]
    sys.stdout.write(' '.join(out) + '\n')


main()