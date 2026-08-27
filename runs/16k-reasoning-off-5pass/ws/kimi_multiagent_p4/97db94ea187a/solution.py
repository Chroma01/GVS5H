import sys
import numpy as np


def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    P = int(data[1])

    V = N - 1            # vertices other than vertex 1
    MMAX = N * (N - 1) // 2
    n_out = MMAX - (N - 1) + 1

    # ---------------- binomial coefficients mod P ----------------
    C = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        C[i][0] = C[i][i] = 1 % P
        for j in range(1, i):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % P

    # general binomial (a choose m) mod P for 0 <= a <= MMAX (a < P always)
    def gen_binom(a, m):
        if m < 0 or m > a:
            return 0
        num = 1
        for r in range(1, m + 1):
            num = num * ((a - m + r) % P) % P
            num = num * pow(r, P - 2, P) % P
        return num

    # ---------------- transition polynomials ----------------
    # Q[t][s][m] = coeff of x^m in ((1+x)^t - 1)^s * (1+x)^(s(s-1)/2)
    Q = [[None] * (V + 1) for _ in range(V + 1)]
    for t in range(1, V + 1):
        for s in range(1, V + 1):
            d = t * s + s * (s - 1) // 2
            poly = [0] * (d + 1)
            for j in range(s + 1):
                cj = C[s][j]
                if (s - j) & 1:
                    cj = (-cj) % P
                tj = t * j
                for m in range(min(tj, d) + 1):
                    v = C[tj][m] if tj <= N else gen_binom(tj, m)
                    poly[m] = (poly[m] + cj * v) % P
            w = s * (s - 1) // 2
            if w:
                pw = [gen_binom(w, m) for m in range(w + 1)]
                new = [0] * (d + 1)
                for a in range(d - w + 1):
                    pa = poly[a]
                    if pa:
                        for b in range(w + 1):
                            new[a + b] = (new[a + b] + pa * pw[b]) % P
                poly = new
            Q[t][s] = np.array(poly, dtype=np.int64)

    # ---------------- layer DP ----------------
    # state[(u, t, p)] -> int64 array [balance idx 0..2u][edges 0..C(u,2)]
    # balance = idx - u ; p = parity of the last layer (L0 has parity 0)
    state = {}
    a0 = np.zeros((1, 1), dtype=np.int64)
    a0[0, 0] = 1 % P
    state[(0, 0, 0)] = a0

    # Overflow safety: each product F*qk < P^2 <= 1e18 < 2^63 (~9.2e18),
    # but accumulating many such products into one cell can exceed 2^63.
    # After ACCUM_LIM additions a cell holds < ACCUM_LIM * 1e18; keep that
    # safely below 2^63 by reducing every ACCUM_LIM k-steps.
    ACCUM_LIM = 8

    for u in range(0, V):
        rem = V - u
        keys = [k for k in state.keys() if k[0] == u]
        for (uu, t, p) in keys:
            F = state[(uu, t, p)]
            if not F.any():
                continue
            fb, fm = F.shape
            for s in range(1, rem + 1):
                q = Q[t][s]
                u2 = uu + s
                m2max = u2 * (u2 - 1) // 2
                key2 = (u2, s, p ^ 1)
                G = state.get(key2)
                if G is None:
                    G = np.zeros((2 * u2 + 1, m2max + 1), dtype=np.int64)
                    state[key2] = G
                # balance shift: new layer parity p^1; even layer -> +s, odd -> -s
                shift = s if (p ^ 1) == 0 else -s
                # target row index = (old balance + shift) + u2 = (idx - uu) + shift + u2
                r0 = shift + u2 - uu
                # convolution along edge axis, vectorized over balance rows,
                # with periodic modular reduction to avoid int64 overflow
                dq = q.shape[0]
                k = 0
                while k < dq:
                    kend = min(k + ACCUM_LIM, dq)
                    for kk in range(k, kend):
                        qk = int(q[kk])
                        if qk == 0:
                            continue
                        G[r0:r0 + fb, kk:kk + fm] += F * qk
                    np.mod(G, P, out=G)
                    k = kend

    # ---------------- collect answer ----------------
    ans = np.zeros(n_out, dtype=np.int64)
    for (u, t, p), F in state.items():
        if u != V:
            continue
        row = F[u]  # balance 0
        take = min(row.shape[0], MMAX + 1)
        if take > N - 1:
            ans[:take - (N - 1)] += row[N - 1:take]
    ans %= P
    sys.stdout.write(" ".join(str(int(x)) for x in ans) + "\n")


solve()