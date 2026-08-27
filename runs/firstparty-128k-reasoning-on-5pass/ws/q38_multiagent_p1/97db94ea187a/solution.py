import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    P = int(data[1])

    H = N // 2
    D = N * (N - 1) // 2
    # No non-root even-distance vertex can be adjacent to vertex 1,
    # so the polynomial degree is at most D - (H - 1).
    R = D - H + 1

    maxF = max(N, D)

    # factorials and inverse factorials
    fact = [1] * (maxF + 1)
    for i in range(1, maxF + 1):
        fact[i] = fact[i - 1] * i % P

    invfact = [1] * (maxF + 1)
    invfact[maxF] = pow(fact[maxF], P - 2, P)
    for i in range(maxF, 0, -1):
        invfact[i - 1] = invfact[i] * i % P

    # modular inverses up to D+1
    inv = [0] * (D + 2)
    inv[1] = 1
    for i in range(2, D + 2):
        inv[i] = (P - P // i) * inv[P % i] % P

    # binomials up to H
    comb = [[0] * (H + 1) for _ in range(H + 1)]
    for n in range(H + 1):
        comb[n][0] = 1
        comb[n][n] = 1
        for k in range(1, n):
            comb[n][k] = (comb[n - 1][k - 1] + comb[n - 1][k]) % P

    # transition terms for every a,b in 1..H:
    # ((1+x)^a - 1)^b * (1+x)^{C(b,2)}
    # = sum_j (-1)^j C(b,j) (1+x)^{C(b,2)+a(b-j)}
    num_trans = H * H
    terms_by_tid = [None] * num_trans
    invfb_by_tid = [0] * num_trans

    for a in range(1, H + 1):
        for b in range(1, H + 1):
            tid = (a - 1) * H + (b - 1)
            base = b * (b - 1) // 2
            terms = []
            for j in range(b + 1):
                coeff = comb[b][j]
                if j & 1:
                    coeff = (-coeff) % P
                exp = base + a * (b - j)
                terms.append((j, coeff, exp))
            terms_by_tid[tid] = tuple(terms)
            invfb_by_tid[tid] = invfact[b]

    # Precompute scalar transition weights for evaluation points x = 0..R.
    # x=0 gives zero for all non-root layers.
    trans_weights = [[0] * num_trans]
    for x in range(1, R + 1):
        z = (x + 1) % P
        powers = [1] * (D + 1)
        for e in range(1, D + 1):
            powers[e] = powers[e - 1] * z % P

        weights = [0] * num_trans
        for tid in range(num_trans):
            s = 0
            for _, coeff, exp in terms_by_tid[tid]:
                s += coeff * powers[exp]
            weights[tid] = (s % P) * invfb_by_tid[tid] % P
        trans_weights.append(weights)

    # DP state: (used_even, used_odd, current_layer_size, current_layer_parity)
    H1 = H + 1
    size = H1 * H1 * H1 * 2

    def idx(e, o, a, p):
        return (((e * H1 + o) * H1 + a) << 1) | p

    start_idx = idx(1, 0, 1, 0)

    states_by_total = [[] for _ in range(N + 1)]
    for e in range(H1):
        if e == 0:
            continue
        for o in range(H1):
            total = e + o
            if total > N:
                continue
            for a in range(1, H1):
                for p in range(2):
                    if p == 0:
                        if e < a:
                            continue
                        q = 1
                        max_b = H - o
                    else:
                        if o < a:
                            continue
                        q = 0
                        max_b = H - e

                    if max_b < 1:
                        continue

                    sidx = idx(e, o, a, p)
                    trans = []
                    if q == 1:
                        for b in range(1, max_b + 1):
                            to = idx(e, o + b, b, 1)
                            tid = (a - 1) * H + (b - 1)
                            trans.append((to, tid))
                    else:
                        for b in range(1, max_b + 1):
                            to = idx(e + b, o, b, 0)
                            tid = (a - 1) * H + (b - 1)
                            trans.append((to, tid))

                    states_by_total[total].append((sidx, tuple(trans)))

    # Flatten in increasing total order. Transitions always increase total.
    active_entries = []
    for t in range(1, N):
        active_entries.extend(states_by_total[t])
    active_entries = tuple(active_entries)

    final_indices = tuple(idx(H, H, a, p) for a in range(1, H1) for p in range(2))

    values = [0] * (R + 1)
    factN1 = fact[N - 1]
    mod = P

    # Evaluate the polynomial at x = 1..R.
    for x in range(1, R + 1):
        dp = [0] * size
        dp[start_idx] = 1
        weights = trans_weights[x]

        for sidx, trans in active_entries:
            val = dp[sidx]
            if val:
                val %= mod
                dp[sidx] = val
                if val:
                    for to, tid in trans:
                        dp[to] += val * weights[tid]

        ans = 0
        for fi in final_indices:
            ans += dp[fi]
        values[x] = (ans % mod) * factN1 % mod

    # Interpolate degree-R polynomial from values at 0..R.
    # Newton forward form: f(x) = sum_k diff[k] * C(x, k).
    cur = values[:]
    diff = [0] * (R + 1)
    for k in range(R + 1):
        diff[k] = cur[0]
        cur = [(cur[i + 1] - cur[i]) % mod for i in range(len(cur) - 1)]

    coeff = [0] * (R + 1)
    B = [1]  # coefficients of C(x, 0)

    for k in range(R + 1):
        d = diff[k]
        if d:
            for m, c in enumerate(B):
                coeff[m] = (coeff[m] + d * c) % mod

        if k < R:
            invk = inv[k + 1]
            new = [0] * (k + 2)
            # B_{k+1} = B_k * (x - k) / (k + 1)
            for i, c in enumerate(B):
                if c:
                    new[i] -= c * k
                    new[i + 1] += c
            for i in range(k + 2):
                new[i] = (new[i] * invk) % mod
            B = new

    out = []
    for M in range(N - 1, D + 1):
        if M <= R:
            out.append(str(coeff[M] % mod))
        else:
            out.append("0")

    sys.stdout.write(" ".join(out) + "\n")


if __name__ == "__main__":
    solve()