import sys

def solve() -> None:
    sys.setrecursionlimit(10000)
    N, P = map(int, sys.stdin.readline().split())
    half = N // 2
    maxM = N * (N - 1) // 2
    max_n = N * N                     # enough for binomials (a*b ≤ N²)

    # ---------- factorials and binomial coefficients ----------
    fact = [1] * (max_n + 1)
    for i in range(1, max_n + 1):
        fact[i] = fact[i - 1] * i % P
    inv_fact = [1] * (max_n + 1)
    inv_fact[max_n] = pow(fact[max_n], P - 2, P)   # Fermat, P is prime
    for i in range(max_n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % P

    def comb(n: int, k: int) -> int:
        if k < 0 or k > n:
            return 0
        return fact[n] * inv_fact[k] % P * inv_fact[n - k] % P

    # ---------- table F[a][b] : bipartite matrices with no zero row ----------
    # F[a][b][e] = number of ways to choose e edges between a left and b right vertices
    #              such that every right vertex has degree ≥ 1.
    F = [[None] * (N + 1) for _ in range(N + 1)]
    F_nonzero = [[None] * (N + 1) for _ in range(N + 1)]
    for a in range(1, N + 1):
        for b in range(1, N + 1):
            limit = min(a * b, maxM)
            f = [0] * (maxM + 1)
            for i in range(0, b + 1):
                coeff = comb(b, i)
                if coeff == 0:
                    continue
                n_rem = (b - i) * a
                max_e_i = min(n_rem, maxM)
                for e in range(0, max_e_i + 1):
                    c = comb(n_rem, e)
                    if c == 0:
                        continue
                    term = coeff * c % P
                    if i & 1:
                        f[e] = (f[e] - term) % P
                    else:
                        f[e] = (f[e] + term) % P
            F[a][b] = f
            nz = [(e, f[e]) for e in range(limit + 1) if f[e] != 0]
            F_nonzero[a][b] = nz

    # ---------- table G[b] : internal edges of a layer of size b ----------
    G = [None] * (N + 1)
    G_nonzero = [None] * (N + 1)
    for b in range(0, N + 1):
        internal = b * (b - 1) // 2
        g = [0] * (maxM + 1)
        for e in range(0, internal + 1):
            g[e] = comb(internal, e)
        G[b] = g
        G_nonzero[b] = [(e, g[e]) for e in range(internal + 1) if g[e] != 0]

    # ---------- table H[s][x] : edges added when a layer of size s is followed by size x ----------
    # H[s][x] = convolution of F[s][x] and G[x]
    H_nonzero = [[None] * (N + 1) for _ in range(N + 1)]
    for s in range(1, N + 1):
        for x in range(1, N + 1):
            h = [0] * (maxM + 1)
            f_list = F_nonzero[s][x]
            g_list = G_nonzero[x]
            for e1, fv in f_list:
                for e2, gv in g_list:
                    e = e1 + e2
                    if e > maxM:
                        break
                    h[e] = (h[e] + fv * gv) % P
            # keep only non‑zero entries, they are generated in increasing order
            nz = [(e, h[e]) for e in range(maxM + 1) if h[e] != 0]
            H_nonzero[s][x] = nz

    # ---------- DP over the layers ----------
    max_edges = [i * (i - 1) // 2 for i in range(N + 1)]   # max possible edges among i vertices

    # dp[t][(e, s, p)] = vector indexed by edge count M
    dp = [dict() for _ in range(N + 1)]
    init_vec = [1]                     # only the root, no edges
    dp[1][(1, 1, 1)] = init_vec        # (even vertices, last layer size, parity of last layer)

    for t in range(1, N):
        cur_dict = dp[t]
        if not cur_dict:
            continue
        remaining = N - t
        for (e, s, parity), cur in cur_dict.items():
            cur_max = max_edges[t]
            # pre‑fetch non‑zero entries of cur (dense, but we avoid zero checks later)
            non_zero = [(idx, cur[idx]) for idx in range(cur_max + 1) if cur[idx] != 0]
            for x in range(1, remaining + 1):
                new_t = t + x
                new_parity = 1 - parity
                new_e = e + (new_parity * x)
                if new_e > half:          # cannot exceed required number of even vertices
                    continue
                factor = comb(remaining, x)
                if factor == 0:
                    continue
                add_list = H_nonzero[s][x]
                if not add_list:
                    continue
                new_max = max_edges[new_t]
                key = (new_e, x, new_parity)
                new_vec = dp[new_t].get(key)
                if new_vec is None:
                    new_vec = [0] * (new_max + 1)
                    dp[new_t][key] = new_vec
                # convolution: new_vec = cur * add * factor
                for e_cur, val_cur in non_zero:
                    max_add = new_max - e_cur
                    inc_base = val_cur * factor % P
                    for add, val_add in add_list:
                        if add > max_add:
                            break
                        new_m = e_cur + add
                        inc = inc_base * val_add % P
                        new_vec[new_m] = (new_vec[new_m] + inc) % P

    # ---------- collect answer ----------
    ans = [0] * (maxM + 1)
    target_e = half
    for (e, s, parity), vec in dp[N].items():
        if e != target_e:
            continue
        for m in range(N - 1, maxM + 1):
            ans[m] = (ans[m] + vec[m]) % P

    out = ' '.join(str(ans[m] % P) for m in range(N - 1, maxM + 1))
    print(out)


if __name__ == "__main__":
    solve()