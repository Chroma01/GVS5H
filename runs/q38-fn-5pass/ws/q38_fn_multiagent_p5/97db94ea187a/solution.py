import sys


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    MOD = int(data[1])

    E = N * (N - 1) // 2

    # The answer polynomial in y=1+x has degree at most
    # E - (N/2 - 1): vertex 1 cannot be adjacent to the other N/2-1
    # even-distance vertices (they are at distance at least 2).
    K = E - (N // 2) + 2

    # Binomial coefficients modulo MOD, up to E.
    comb = [[0] * (E + 1) for _ in range(E + 1)]
    for n in range(E + 1):
        comb[n][0] = 1
        comb[n][n] = 1
        for k in range(1, n):
            comb[n][k] = (comb[n - 1][k - 1] + comb[n - 1][k]) % MOD

    stride = N + 1

    # Groups are (used_vertices u, parity difference d=even-odd, last_parity p).
    # For each group we keep a vector indexed by last_layer_size t.
    key_to_idx = {}
    gu = []
    gd = []
    gp = []
    masks = []
    outs_temp = []
    by_u = [[] for _ in range(N + 1)]

    def get_group(u, d, p):
        key = (u, d, p)
        idx = key_to_idx.get(key)
        if idx is None:
            idx = len(gu)
            key_to_idx[key] = idx
            gu.append(u)
            gd.append(d)
            gp.append(p)
            masks.append(0)
            outs_temp.append([])
            by_u[u].append(idx)
        return idx

    start = get_group(1, 1, 0)  # vertex 1 is the only even layer-0 vertex
    masks[start] = 1 << 1

    # Build reachable groups and aggregated transitions.
    for u in range(1, N):
        for idx in by_u[u]:
            if masks[idx] == 0:
                continue
            d = gd[idx]
            p = gp[idx]
            rem = N - u
            np = 1 - p
            for s in range(1, rem + 1):
                lab = comb[rem][s]
                if lab == 0:
                    continue
                nd = d + s if np == 0 else d - s
                if abs(nd) > N - (u + s):
                    continue
                to = get_group(u + s, nd, np)
                masks[to] |= 1 << s
                outs_temp[idx].append((to, s, lab))

    G = len(gu)

    order = []
    for u in range(1, N + 1):
        order.extend(by_u[u])

    offs = [g * stride for g in range(G)]

    outs = []
    for idx in range(G):
        # Store final flat position directly: target_offset + new_last_size.
        outs.append([(to * stride + s, s, lab) for to, s, lab in outs_temp[idx]])

    t_lists = []
    for mask in masks:
        lst = []
        for t in range(1, N + 1):
            if (mask >> t) & 1:
                lst.append(t)
        t_lists.append(lst)

    full_groups = by_u[N]
    full_info = [(offs[g], t_lists[g]) for g in full_groups]

    group_infos = []
    for g in order:
        if outs[g]:
            group_infos.append((offs[g], t_lists[g], outs[g]))

    start_pos = offs[start] + 1
    dp_size = G * stride

    C2 = [s * (s - 1) // 2 for s in range(N + 1)]
    max_pow = E

    vals = []

    # Evaluate the y-polynomial at y = 0, 1, ..., K-1.
    for z in range(K):
        # At y=1 (x=0) there are no connected graphs with N>=2 vertices.
        if z == 1:
            vals.append(0)
            continue

        if z == 0:
            pow_z = [1] + [0] * max_pow
        else:
            pow_z = [1] * (max_pow + 1)
            for i in range(1, max_pow + 1):
                pow_z[i] = (pow_z[i - 1] * z) % MOD

        powC2 = [pow_z[c] for c in C2]

        # base_by_s[s][t] = z^{C(s,2)} * (z^t - 1)^s
        base_by_s = [[0] * (N + 1) for _ in range(N + 1)]
        for t in range(1, N + 1):
            a = pow_z[t] - 1
            if a < 0:
                a += MOD
            val = 1
            for s in range(1, N + 1):
                val = (val * a) % MOD
                if val:
                    pc = powC2[s]
                    if pc:
                        base_by_s[s][t] = (val * pc) % MOD

        dp = [0] * dp_size
        dp[start_pos] = 1

        # Topological DP over used vertices.
        for off, tlist, outs_g in group_infos:
            nz = []
            for t in tlist:
                vt = dp[off + t]
                if vt:
                    nz.append((t, vt))
            if not nz:
                continue

            for pos, s, lab in outs_g:
                bs = base_by_s[s]
                total = 0
                for t, vt in nz:
                    total += vt * bs[t]
                if total:
                    dp[pos] = (dp[pos] + total * lab) % MOD

        ans = 0
        for off, tlist in full_info:
            for t in tlist:
                ans += dp[off + t]
        vals.append(ans % MOD)

    # Modular inverses 1..K.
    inv = [0] * (K + 1)
    if K >= 1:
        inv[1] = 1
    for i in range(2, K + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # Newton interpolation from values at 0,1,...,K-1 to coefficients in y.
    cur = vals[:]
    coeff_y = [0] * K
    binom_poly = [1]  # C(y, 0)

    for j in range(K):
        c = cur[0]
        if c:
            for k, coef in enumerate(binom_poly):
                if coef:
                    coeff_y[k] = (coeff_y[k] + c * coef) % MOD

        for i in range(K - 1 - j):
            cur[i] = (cur[i + 1] - cur[i]) % MOD

        if j + 1 < K:
            invj = inv[j + 1]
            new_poly = [0] * (len(binom_poly) + 1)
            for k, coef in enumerate(binom_poly):
                if coef:
                    new_poly[k] = (new_poly[k] - coef * j) % MOD
                    new_poly[k + 1] = (new_poly[k + 1] + coef) % MOD
            if invj != 1:
                for k in range(len(new_poly)):
                    new_poly[k] = (new_poly[k] * invj) % MOD
            binom_poly = new_poly

    # Convert F(y) to G(x)=F(1+x):
    # [x^m] G = sum_k coeff_y[k] * C(k, m).
    res = []
    for m in range(N - 1, E + 1):
        if m >= K:
            res.append("0")
        else:
            total = 0
            for k in range(m, K):
                total = (total + coeff_y[k] * comb[k][m]) % MOD
            res.append(str(total))

    sys.stdout.write(" ".join(res) + "\n")


if __name__ == "__main__":
    main()