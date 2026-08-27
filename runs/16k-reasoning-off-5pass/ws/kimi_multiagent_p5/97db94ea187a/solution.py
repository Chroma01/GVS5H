import sys
import numpy as np


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    P = int(data[1])
    K = N // 2
    MAXN = N * (N - 1) // 2  # up to 435

    # ---------- binomials mod P via Pascal ----------
    binom = [[0] * (MAXN + 1) for _ in range(MAXN + 1)]
    binom[0][0] = 1 % P
    for n in range(1, MAXN + 1):
        row = binom[n]
        prev = binom[n - 1]
        row[0] = 1 % P
        for k in range(1, n + 1):
            row[k] = (prev[k - 1] + prev[k]) % P
    binom_np = [np.array(binom[n][:n + 1], dtype=np.int64) for n in range(MAXN + 1)]

    MASK = 32767  # 2^15 - 1

    def conv_mod(a, b):
        # convolution mod P; entries of a,b are < P < 2^30
        la, lb = len(a), len(b)
        if la == 0 or lb == 0:
            return np.zeros(0, dtype=np.int64)
        # make b the shorter operand (fewer int64 multiplications)
        if la < lb:
            a, b = b, a
            la, lb = lb, la
        blo = b & MASK
        bhi = b >> 15
        lo = np.convolve(a, blo)
        hi = np.convolve(a, bhi)
        # entries: a < 2^30, blo < 2^15 -> products < 2^45,
        # sums over <= 436 terms < 2^54 (safe in int64)
        return (lo % P + (hi % P) * 32768) % P

    # ---------- covering polynomials A(s,t) and transitions T(s,t) ----------
    # A(s,t,m) = sum_j (-1)^j C(t,j) C(s*(t-j), m): every one of the t new
    # vertices has at least one neighbor among the s previous-layer vertices.
    T = [[None] * (N + 1) for _ in range(N + 1)]
    for s in range(1, N):
        for t in range(1, N - s + 1):
            A = np.zeros(s * t + 1, dtype=np.int64)
            bt = binom[t]
            for j in range(t + 1):
                row = binom_np[s * (t - j)]
                c = bt[j] % P
                if j & 1:
                    A[:len(row)] = (A[:len(row)] - c * row) % P
                else:
                    A[:len(row)] = (A[:len(row)] + c * row) % P
            W = binom_np[t * (t - 1) // 2]  # within-new-layer edges
            T[s][t] = conv_mod(A, W)

    # ---------- DP over BFS layerings ----------
    # state (u, s, p, d) -> numpy poly over edge count:
    #   u = vertices placed so far, s = size of last layer,
    #   p = parity of last layer index,
    #   d = (#even-distance vertices) - (#odd-distance vertices) so far.
    # Initial layer L0 = {1}: u=1, s=1, p=0, d=1.
    dp = {(1, 1, 0, 1): np.array([1], dtype=np.int64)}

    for u in range(1, N):
        R = N - u
        dmax_u = min(u, R, K)
        for s in range(1, u + 1):
            for p in (0, 1):
                for d in range(-dmax_u, dmax_u + 1):
                    f = dp.get((u, s, p, d))
                    if f is None:
                        continue
                    np_ = 1 - p  # parity of the new layer
                    Ts = T[s]
                    brow = binom[R]
                    for t in range(1, R + 1):
                        nd = d + t if np_ == 0 else d - t
                        u2 = u + t
                        rem = R - t
                        if nd > rem or nd < -rem:
                            continue
                        e = (u2 + nd) // 2
                        if e > K or u2 - e > K:
                            continue
                        lab = brow[t] % P
                        conv = conv_mod(f, Ts[t])
                        if lab != 1:
                            conv = conv * lab % P
                        key = (u2, t, np_, nd)
                        old = dp.get(key)
                        if old is None:
                            dp[key] = conv
                        else:
                            if len(old) < len(conv):
                                old, conv = conv, old
                            old[:len(conv)] += conv
                            dp[key] = old % P

    # ---------- collect answers ----------
    ans = np.zeros(MAXN + 1, dtype=np.int64)
    for (u, s, p, d), f in dp.items():
        if u == N and d == 0:
            m = len(f)
            ans[:m] = (ans[:m] + f) % P

    out = " ".join(str(int(ans[M] % P)) for M in range(N - 1, MAXN + 1))
    sys.stdout.write(out + "\n")


main()