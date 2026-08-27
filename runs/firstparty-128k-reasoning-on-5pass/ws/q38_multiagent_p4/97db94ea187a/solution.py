import sys
import gc


def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    gc.disable()

    N = int(data[0])
    P = int(data[1])

    H = N // 2
    Emax = H - 1
    total_edges = N * (N - 1) // 2
    D = total_edges - H + 1

    # factorials and inverse factorials modulo P
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % P

    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], P - 2, P)
    for i in range(N, 0, -1):
        invfact[i - 1] = invfact[i] * i % P

    fact_nm1 = fact[N - 1]

    # Build reachable and feasible BFS-layer states.
    # state: (o, e, p, par)
    # o: total size of odd-distance non-root layers
    # e: total size of even-distance non-root layers
    # p: size of the last layer
    # par: 0 = last layer even (root initially), 1 = last layer odd
    states = []
    idx_map = {}

    def add_state(o, e, p, par):
        key = (o, e, p, par)
        if key not in idx_map:
            idx_map[key] = len(states)
            states.append(key)

    # root
    add_state(0, 0, 1, 0)

    # par = 0, non-root even last layer
    for e in range(1, Emax + 1):
        o_max = H if e == Emax else H - 1
        for o in range(1, o_max + 1):
            if o == 1:
                p_vals = (e,)
            else:
                p_vals = range(1, e + 1)
            for p in p_vals:
                add_state(o, e, p, 0)

    # par = 1, odd last layer
    # e = 0: only one odd layer, so p = o
    for o in range(1, H + 1):
        add_state(o, 0, o, 1)

    # 0 < e < Emax: need at least one previous odd layer, so p <= o-1
    for e in range(1, Emax):
        for o in range(2, H + 1):
            for p in range(1, o):
                add_state(o, e, p, 1)

    # final odd layer: e = Emax, o = H, p < H (unless H=1 handled above)
    if Emax > 0:
        for p in range(1, H):
            add_state(H, Emax, p, 1)

    S = len(states)
    L = H
    stride = L + 1

    # Precompute transitions and weight offsets.
    trans = [[] for _ in range(S)]
    for idx, (o, e, p, par) in enumerate(states):
        if par == 0:
            if o == H and e == Emax:
                continue
            max_a = H - o
            base = p * stride
            for a in range(1, max_a + 1):
                t = idx_map.get((o + a, e, a, 1))
                if t is not None:
                    trans[idx].append((t, base + a))
        else:
            if o == H and e == Emax:
                continue
            max_b = Emax - e
            if max_b <= 0:
                continue
            base = p * stride
            if o == H:
                b = max_b
                t = idx_map.get((H, Emax, b, 0))
                if t is not None:
                    trans[idx].append((t, base + b))
            else:
                for b in range(1, max_b + 1):
                    t = idx_map.get((o, e + b, b, 0))
                    if t is not None:
                        trans[idx].append((t, base + b))

    order = [
        i for i in sorted(range(S), key=lambda i: states[i][0] + states[i][1])
        if trans[i]
    ]
    final_indices = [
        i for i, (o, e, p, par) in enumerate(states)
        if o == H and e == Emax
    ]
    init_idx = idx_map[(0, 0, 1, 0)]

    vals = [0] * (D + 1)  # vals[0] = 0
    s_range = range(1, L + 1)
    p_range = range(1, L + 1)
    w_size = stride * stride

    # Evaluate F(x) at x = 1..D.
    for x in range(1, D + 1):
        z = (x + 1) % P

        # coef[s] = z^{C(s,2)} / s!
        coef = [0] * (L + 1)
        zpow_c = 1
        add_pow = 1
        for s in s_range:
            zpow_c = (zpow_c * add_pow) % P
            coef[s] = (zpow_c * invfact[s]) % P
            add_pow = (add_pow * z) % P

        # w[p, s] = z^{C(s,2)} * (z^p - 1)^s / s!
        w = [0] * w_size
        zp = 1
        for p in p_range:
            zp = (zp * z) % P
            base_val = zp - 1
            if base_val < 0:
                base_val += P
            if base_val == 0:
                continue
            pow_base = 1
            base_idx = p * stride
            for s in s_range:
                pow_base = (pow_base * base_val) % P
                w[base_idx + s] = (pow_base * coef[s]) % P

        dp = [0] * S
        dp[init_idx] = 1

        dp_list = dp
        w_list = w
        trans_list = trans
        P_local = P

        for idx in order:
            val = dp_list[idx]
            if val:
                if val >= P_local:
                    val %= P_local
                if val:
                    for t, off in trans_list[idx]:
                        dp_list[t] += val * w_list[off]

        ssum = 0
        for fi in final_indices:
            ssum += dp_list[fi]

        vals[x] = (ssum % P) * fact_nm1 % P

    # Interpolate vals[0..D] into power basis.
    # Newton forward form: F(x) = sum c[k] * C(x, k), c[k] = Δ^k F(0).
    diff = vals[:]
    c = [0] * (D + 1)
    for k in range(D + 1):
        c[k] = diff[0]
        for i in range(D - k):
            diff[i] = (diff[i + 1] - diff[i]) % P

    inv = [0] * (D + 1)
    if D >= 1:
        inv[1] = 1
        for i in range(2, D + 1):
            inv[i] = (P - (P // i)) * inv[P % i] % P

    ans = [0] * (D + 1)
    row = [1]  # coefficients of C(x, 0)
    ans[0] = c[0]

    for k in range(1, D + 1):
        km1 = k - 1
        invk = inv[k]
        new = [0] * (k + 1)

        if km1:
            new[0] = (-km1 * row[0]) % P
        else:
            new[0] = 0
        new[0] = (new[0] * invk) % P

        for m in range(1, k):
            new[m] = (row[m - 1] - km1 * row[m]) % P
            new[m] = (new[m] * invk) % P

        new[k] = (row[k - 1] * invk) % P
        row = new

        ck = c[k]
        if ck:
            for m in range(k + 1):
                ans[m] += ck * row[m]

    for i in range(D + 1):
        ans[i] %= P

    out = []
    for M in range(N - 1, total_edges + 1):
        if M <= D:
            out.append(str(ans[M]))
        else:
            out.append("0")

    sys.stdout.write(" ".join(out) + "\n")


if __name__ == "__main__":
    solve()