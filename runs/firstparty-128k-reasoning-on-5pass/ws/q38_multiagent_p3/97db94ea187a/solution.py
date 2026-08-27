import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    P = int(data[1])

    U = N - 1                  # non-root vertices
    E = N // 2 - 1             # required even-distance non-root vertices
    C = N * (N - 1) // 2
    max_valid = C - N // 2 + 1
    K = max_valid - (N - 1) + 1

    # factorials and inverse factorials
    maxF = max(N, K)
    fact = [1] * (maxF + 1)
    for i in range(1, maxF + 1):
        fact[i] = fact[i - 1] * i % P
    invfact = [1] * (maxF + 1)
    invfact[maxF] = pow(fact[maxF], P - 2, P)
    for i in range(maxF, 0, -1):
        invfact[i - 1] = invfact[i] * i % P

    # modular inverses of 1..K
    inv = [0] * (K + 1)
    if K >= 1:
        inv[1] = 1
        for i in range(2, K + 1):
            inv[i] = (P - P // i) * inv[P % i] % P

    # inverse of x^(N-1) for x = 1..K
    inv_x_pow = [0] * (K + 1)
    for x in range(1, K + 1):
        inv_x_pow[x] = pow(inv[x], U, P)

    # state indexing: (next_parity, even_count, used, last_layer_size)
    A = U + 1
    E1 = E + 1
    S = 2 * E1 * A * A

    def get_idx(p, e, u, a):
        return (((p * E1 + e) * A + u) * A + a)

    valid = [False] * S
    idx_to_comp = [-1] * S
    comp_to_idx = []
    states_by_u = [[] for _ in range(U + 1)]
    p_arr = []
    e_arr = []
    a_arr = []
    final_comps = []

    # Generate only states that are reachable and can still be extended.
    for u in range(U + 1):
        R = U - u
        for p in (0, 1):
            if u == 0:
                if p != 1:
                    continue
            else:
                if p == 1 and u < 2:
                    continue

            if R == 0:
                min_add = 0
                max_add = 0
            else:
                if p == 1:
                    min_add = 0
                    max_add = R - 1 if R >= 2 else 0
                else:
                    min_add = 1
                    max_add = R

            e_min = E - max_add
            if e_min < 0:
                e_min = 0
            e_max = E
            if u < e_max:
                e_max = u
            em = E - min_add
            if em < e_max:
                e_max = em
            if u > 0 and e_max > u - 1:
                e_max = u - 1
            if e_min > e_max:
                continue

            for e in range(e_min, e_max + 1):
                if u == 0:
                    a_list = [1]
                else:
                    O = u - e  # odd-distance non-root vertices so far
                    if p == 0:
                        if e == 0:
                            a_list = [u]
                        else:
                            if O < 2:
                                continue
                            a_max = O - 1
                            if a_max < 1:
                                continue
                            a_list = range(1, a_max + 1)
                    else:
                        if e < 1 or O < 1:
                            continue
                        if O == 1:
                            a_list = [e]
                        else:
                            a_max = e
                            if a_max < 1:
                                continue
                            a_list = range(1, a_max + 1)

                for a in a_list:
                    idx = get_idx(p, e, u, a)
                    if not valid[idx]:
                        valid[idx] = True
                        comp = len(comp_to_idx)
                        idx_to_comp[idx] = comp
                        comp_to_idx.append(idx)
                        states_by_u[u].append(comp)
                        p_arr.append(p)
                        e_arr.append(e)
                        a_arr.append(a)
                        if u == U and e == E:
                            final_comps.append(comp)

    Sv = len(comp_to_idx)
    start_comp = idx_to_comp[get_idx(1, 0, 0, 1)]

    # Precompute transitions.
    trans = [[] for _ in range(Sv)]
    for u in range(U):
        for comp in states_by_u[u]:
            p = p_arr[comp]
            e = e_arr[comp]
            a = a_arr[comp]
            max_s = U - u
            if p == 0:
                rem = E - e
                if rem < max_s:
                    max_s = rem
            if max_s <= 0:
                continue
            for s in range(1, max_s + 1):
                e2 = e + (s if p == 0 else 0)
                to_idx = get_idx(1 - p, e2, u + s, s)
                if valid[to_idx]:
                    to_comp = idx_to_comp[to_idx]
                    trans[comp].append((to_comp, a * A + s))

    for u in range(U):
        if states_by_u[u]:
            states_by_u[u] = tuple(c for c in states_by_u[u] if trans[c])
        else:
            states_by_u[u] = ()
    final_comps = tuple(final_comps)
    for i in range(Sv):
        trans[i] = tuple(trans[i]) if trans[i] else ()

    invfact_s = invfact[:A]
    fact_U = fact[U]

    # Evaluate A(x) at x = 1..K, then G(x)=A(x)/x^(N-1).
    vals = []
    P_local = P
    A_local = A
    U_local = U
    trans_local = trans
    states_by_u_local = states_by_u
    Sv_local = Sv
    start_local = start_comp
    final_local = final_comps
    fact_U_local = fact_U
    inv_x_pow_local = inv_x_pow
    invfact_s_local = invfact_s

    for x in range(1, K + 1):
        y = x + 1
        if y >= P_local:
            y %= P_local

        pow_y = [1] * A_local
        for i in range(1, A_local):
            pow_y[i] = (pow_y[i - 1] * y) % P_local

        # ipc[s] = invfact[s] * y^{s(s-1)/2}
        ipc = [1] * A_local
        pc = 1
        for s in range(1, A_local):
            if s > 1:
                pc = (pc * pow_y[s - 1]) % P_local
            ipc[s] = (invfact_s_local[s] * pc) % P_local

        # W[a*A+s] = invfact[s] * y^{C(s,2)} * (y^a - 1)^s
        W = [0] * (A_local * A_local)
        for a in range(1, A_local):
            base = pow_y[a] - 1
            if base < 0:
                base += P_local
            if base == 0:
                continue
            val = 1
            row = a * A_local
            for s in range(1, A_local):
                val = (val * base) % P_local
                W[row + s] = (ipc[s] * val) % P_local

        dp = [0] * Sv_local
        dp[start_local] = 1

        for u in range(U_local):
            for comp in states_by_u_local[u]:
                val = dp[comp]
                if val:
                    if val >= P_local:
                        val %= P_local
                    if val:
                        for to, widx in trans_local[comp]:
                            dp[to] += val * W[widx]

        ans = 0
        for comp in final_local:
            ans += dp[comp]
        ans %= P_local
        ans = (ans * fact_U_local) % P_local
        vals.append((ans * inv_x_pow_local[x]) % P_local)

    # Interpolate G from points 1..K.
    # H(z)=G(1+z), H(z)=sum h[k] C(z,k), then convert C(x-1,k) to powers of x.
    diff = vals[:]
    h = [0] * K
    for k in range(K):
        h[k] = diff[0] % P_local
        for i in range(K - k - 1):
            v = diff[i + 1] - diff[i]
            if v < 0:
                v += P_local
            diff[i] = v

    coeff = [0] * K
    basis = [1]  # coefficients of C(x-1,k) in powers of x
    for k in range(K):
        hk = h[k]
        if hk:
            for j, bj in enumerate(basis):
                coeff[j] = (coeff[j] + hk * bj) % P_local
        if k == K - 1:
            break

        kk = k + 1
        new = [0] * (kk + 1)
        for j, bj in enumerate(basis):
            new[j] = (new[j] - kk * bj) % P_local
            new[j + 1] = (new[j + 1] + bj) % P_local
        invk = inv[kk]
        if invk != 1:
            for j in range(kk + 1):
                new[j] = (new[j] * invk) % P_local
        basis = new

    out = [str(coeff[d] % P_local) for d in range(K)]
    zeros = C - max_valid
    if zeros:
        out.extend(['0'] * zeros)
    sys.stdout.write(' '.join(out) + '\n')


if __name__ == "__main__":
    solve()