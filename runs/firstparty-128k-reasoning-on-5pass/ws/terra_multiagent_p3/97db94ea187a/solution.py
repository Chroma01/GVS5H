import sys

def solve():
    N, MOD = map(int, sys.stdin.readline().split())
    h = N // 2
    total_edges = N * (N - 1) // 2

    # Maximum possible number of edges among valid balanced BFS layerings.
    # Achieved by layer sizes [1, h, h-1].
    deg = 2 * h * h - 2 * h + 1

    # Binomial coefficients for label assignment transitions.
    comb = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        comb[i][0] = comb[i][i] = 1
        for j in range(1, i):
            comb[i][j] = (comb[i - 1][j - 1] + comb[i - 1][j]) % MOD

    # State: (number in even layers, number in odd layers, last layer size, last parity)
    # parity 0 = even, 1 = odd.
    states = [(1, 0, 1, 0)]  # root vertex alone
    for e in range(1, h + 1):
        for o in range(1, h + 1):
            # A non-root even final layer cannot contain the root, hence size <= e-1.
            for a in range(1, e):
                states.append((e, o, a, 0))
            for a in range(1, o + 1):
                states.append((e, o, a, 1))

    states.sort(key=lambda z: (z[0] + z[1], z[3], z[0], z[1], z[2]))
    state_id = {s: i for i, s in enumerate(states)}
    root_id = state_id[(1, 0, 1, 0)]

    # Each transition appends one nonempty BFS layer.
    # (source id, destination id, previous layer size, new layer size, label factor)
    transitions = []
    for sid, (e, o, a, parity) in enumerate(states):
        used = e + o
        if parity == 0:
            # Append an odd layer.
            for b in range(1, h - o + 1):
                dst = state_id[(e, o + b, b, 1)]
                transitions.append((sid, dst, a, b, comb[N - used][b]))
        else:
            # Append an even layer.
            for b in range(1, h - e + 1):
                dst = state_id[(e + b, o, b, 0)]
                transitions.append((sid, dst, a, b, comb[N - used][b]))

    final_ids = []
    for sid, (e, o, a, parity) in enumerate(states):
        if e == h and o == h:
            final_ids.append(sid)

    values = [0] * (deg + 1)
    max_b = h
    max_a = h

    # Evaluate the desired polynomial at x = 0, 1, ..., deg.
    for x in range(deg + 1):
        q = (x + 1) % MOD

        qpow = [1] * (N + 1)
        for k in range(1, N + 1):
            qpow[k] = qpow[k - 1] * q % MOD

        # g[a][b] =
        # (1+x)^(C(b,2)) * (((1+x)^a - 1)^b)
        # for appending a layer of size b after a layer of size a.
        g = [[0] * (max_b + 1) for _ in range(max_a + 1)]
        for a in range(1, max_a + 1):
            base = (qpow[a] - 1) % MOD
            pw = 1
            for b in range(1, max_b + 1):
                pw = pw * base % MOD
                g[a][b] = pw * qpow[b * (b - 1) // 2] % MOD

        dp = [0] * len(states)
        dp[root_id] = 1

        for src, dst, a, b, label_factor in transitions:
            cur = dp[src]
            if cur:
                dp[dst] = (dp[dst] + cur * label_factor % MOD * g[a][b]) % MOD

        values[x] = sum(dp[i] for i in final_ids) % MOD

    # Interpolate from values at 0,1,...,deg.
    # P(x) = sum_k Delta^k P(0) * binom(x,k).
    fact = [1] * (deg + 1)
    for i in range(1, deg + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (deg + 1)
    invfact[deg] = pow(fact[deg], MOD - 2, MOD)
    for i in range(deg, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    ans = [0] * (deg + 1)
    diff = values[:]
    basis = [1]  # falling factorial x(x-1)...(x-k+1)

    for k in range(deg + 1):
        coef = diff[0] * invfact[k] % MOD
        for i, v in enumerate(basis):
            ans[i] = (ans[i] + coef * v) % MOD

        if k < deg:
            ndiff = [0] * (len(diff) - 1)
            for i in range(len(ndiff)):
                ndiff[i] = (diff[i + 1] - diff[i]) % MOD
            diff = ndiff

            nb = [0] * (len(basis) + 1)
            for i, v in enumerate(basis):
                nb[i] = (nb[i] - k * v) % MOD
                nb[i + 1] = (nb[i + 1] + v) % MOD
            basis = nb

    out = []
    for m in range(N - 1, total_edges + 1):
        out.append(str(ans[m] if m <= deg else 0))
    print(" ".join(out))

if __name__ == "__main__":
    solve()