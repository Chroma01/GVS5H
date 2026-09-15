import sys
import gc


def solve():
    gc.disable()
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    MOD = int(data[1])

    H = N // 2
    D = N * (N - 1) // 2

    # Binomial coefficients modulo MOD.
    C = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        C[i][0] = 1
        C[i][i] = 1
        for j in range(1, i):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD

    # State: (used_even, used_odd, last_layer_size, next_parity)
    # next_parity: 1 = odd layer, 0 = even layer.
    # used_even includes vertex 1.
    start = (1, 0, 1, 1)
    state_to_id = {start: 0}
    states = [start]
    queue = [0]
    trans_raw = []

    head = 0
    while head < len(queue):
        sid = queue[head]
        head += 1
        e, o, a, p = states[sid]
        s = e + o
        if s == N:
            continue

        limit = H - o if p == 1 else H - e
        maxb = N - s
        if limit < maxb:
            maxb = limit

        for b in range(1, maxb + 1):
            if p == 1:
                ne, no = e, o + b
            else:
                ne, no = e + b, o

            to_state = (ne, no, b, 1 - p)
            tid = state_to_id.get(to_state)
            if tid is None:
                tid = len(states)
                state_to_id[to_state] = tid
                states.append(to_state)
                queue.append(tid)

            comb = C[N - s][b]
            deg = b * (b - 1) // 2 + a * b
            trans_raw.append((sid, tid, a, b, comb, deg))

    num_states = len(states)

    terminal_ids = [
        i for i, (e, o, a, p) in enumerate(states)
        if e == H and o == H
    ]

    # Keep only states that can reach a terminal state.
    rev = [[] for _ in range(num_states)]
    for sid, tid, a, b, comb, deg in trans_raw:
        rev[tid].append(sid)

    good = [False] * num_states
    q = []
    for tid in terminal_ids:
        if not good[tid]:
            good[tid] = True
            q.append(tid)

    head = 0
    while head < len(q):
        cur = q[head]
        head += 1
        for pre in rev[cur]:
            if not good[pre]:
                good[pre] = True
                q.append(pre)

    trans = []
    for tr in trans_raw:
        if good[tr[0]] and good[tr[1]]:
            trans.append(tr)

    order = sorted(
        (i for i in range(num_states) if good[i]),
        key=lambda i: states[i][0] + states[i][1]
    )

    # Group transitions by (a, b, comb), because the scalar factor for a
    # fixed evaluation point depends only on these three values.
    key_map = {}
    key_a = []
    key_b = []
    key_comb = []
    trans_key = []

    for sid, tid, a, b, comb, deg in trans:
        key = (a, b, comb)
        kid = key_map.get(key)
        if kid is None:
            kid = len(key_a)
            key_map[key] = kid
            key_a.append(a)
            key_b.append(b)
            key_comb.append(comb)
        trans_key.append(kid)

    num_keys = len(key_a)
    stride = H + 1
    key_ab_idx = [key_a[i] * stride + key_b[i] for i in range(num_keys)]

    adj = [[] for _ in range(num_states)]
    adj_deg = [[] for _ in range(num_states)]

    for (sid, tid, a, b, comb, deg), kid in zip(trans, trans_key):
        adj[sid].append((tid, kid))
        adj_deg[sid].append((tid, deg))

    order_proc = [i for i in order if adj[i]]

    # Maximum possible degree of the answer polynomial.
    maxdeg = [-1] * num_states
    maxdeg[0] = 0
    for sid in order:
        md = maxdeg[sid]
        if md < 0:
            continue
        for to, deg in adj_deg[sid]:
            nm = md + deg
            if nm > maxdeg[to]:
                maxdeg[to] = nm

    maxE = 0
    for tid in terminal_ids:
        if good[tid] and maxdeg[tid] > maxE:
            maxE = maxdeg[tid]

    L = max(maxE, N - 1)
    if L > D:
        L = D

    # For evaluation at x=t, only powers (1+t)^k with k <= max(H, C(H,2))
    # are needed.
    max_exp = max(H, H * (H - 1) // 2)
    exp_b = [b * (b - 1) // 2 for b in range(H + 1)]

    pow_base = [0] * (max_exp + 1)
    internal = [0] * (H + 1)
    parent = [0] * ((H + 1) * stride)
    factors = [0] * num_keys

    vals = [0] * (L + 1)  # vals[0] = F(0) = 0

    LIMIT = 1 << 63

    key_b_l = key_b
    key_ab_l = key_ab_idx
    key_comb_l = key_comb
    adj_l = adj
    order_proc_l = order_proc
    terminal_ids_l = terminal_ids

    for t in range(1, L + 1):
        base = (t + 1) % MOD

        pb = pow_base
        pb[0] = 1
        for i in range(1, max_exp + 1):
            pb[i] = (pb[i - 1] * base) % MOD

        for b in range(H + 1):
            internal[b] = pb[exp_b[b]]

        for a in range(1, H + 1):
            v = pb[a] - 1
            if v < 0:
                v += MOD
            val = 1
            idx = a * stride
            for b in range(H + 1):
                parent[idx + b] = val
                val = (val * v) % MOD

        for i in range(num_keys):
            b = key_b_l[i]
            factors[i] = (
                parent[key_ab_l[i]] * internal[b] % MOD
            ) * key_comb_l[i] % MOD

        dp = [0] * num_states
        dp[0] = 1

        dp_l = dp
        factors_l = factors
        MOD_l = MOD
        LIMIT_l = LIMIT

        for sid in order_proc_l:
            val = dp_l[sid]
            if val:
                val %= MOD_l
                if val:
                    for to, kid in adj_l[sid]:
                        nv = dp_l[to] + val * factors_l[kid]
                        if nv >= LIMIT_l:
                            nv %= MOD_l
                        dp_l[to] = nv

        ans = 0
        for tid in terminal_ids_l:
            ans += dp[tid]
        vals[t] = ans % MOD

    # Newton forward differences.
    diff = vals[:]
    d = []
    for k in range(L + 1):
        d.append(diff[0])
        if k < L:
            diff = [(diff[i + 1] - diff[i]) % MOD for i in range(len(diff) - 1)]

    # Modular inverses of 1..L.
    inv = [0] * (L + 1)
    if L >= 1:
        inv[1] = 1
        for i in range(2, L + 1):
            inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # Convert from binomial basis sum d[k] * C(x, k) to standard powers.
    coeff = [0] * (L + 1)
    coeff[0] = d[0] % MOD
    old = [1]

    for k in range(1, L + 1):
        km1 = k - 1
        invk = inv[k]
        new = [0] * (k + 1)

        new[0] = (-km1 * old[0]) % MOD
        for j in range(1, k):
            new[j] = (old[j - 1] - km1 * old[j]) % MOD
        new[k] = old[k - 1]

        dk = d[k]
        if dk:
            for j in range(k + 1):
                new[j] = (new[j] * invk) % MOD
                coeff[j] = (coeff[j] + dk * new[j]) % MOD
        else:
            for j in range(k + 1):
                new[j] = (new[j] * invk) % MOD

        old = new

    out = []
    for m in range(N - 1, D + 1):
        if m <= L:
            out.append(str(coeff[m] % MOD))
        else:
            out.append("0")

    sys.stdout.write(" ".join(out) + "\n")


if __name__ == "__main__":
    solve()