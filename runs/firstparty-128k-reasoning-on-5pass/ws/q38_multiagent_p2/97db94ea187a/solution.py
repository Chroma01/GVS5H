import sys
import gc


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    gc.disable()

    N = int(data[0])
    MOD = int(data[1])
    half = N // 2

    max_extra = (N - 1) * (N - 2) // 2
    D = max_extra + 1

    stride = N
    A = N * N

    maxF = max(N, D)
    fact = [1] * (maxF + 1)
    for i in range(1, maxF + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact = [1] * (maxF + 1)
    invfact[maxF] = pow(fact[maxF], MOD - 2, MOD)
    for i in range(maxF, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # mask0/1[s][e] has bit a set iff state (s, e, parity, a) is reachable
    # and can still finish.
    mask0 = [[0] * (half + 1) for _ in range(N + 1)]
    mask1 = [[0] * (half + 1) for _ in range(N + 1)]
    mask0[1][1] = 1 << 1

    for s in range(1, N):
        r = N - s
        for e in range(half + 1):
            m0 = mask0[s][e]
            if m0:
                d = half - e
                if d == 0:
                    b = r
                    if b >= 1:
                        mask1[s + b][e] |= 1 << b
                elif 0 < d < r:
                    bmax = r - d
                    for b in range(1, bmax + 1):
                        mask1[s + b][e] |= 1 << b

            m1 = mask1[s][e]
            if m1:
                d = half - e
                if d == r:
                    b = r
                    if b >= 1:
                        mask0[s + b][e + b] |= 1 << b
                elif 0 < d < r:
                    for b in range(1, d + 1):
                        mask0[s + b][e + b] |= 1 << b

    idx0 = [[[-1] * (N + 1) for _ in range(half + 1)] for _ in range(N + 1)]
    idx1 = [[[-1] * (N + 1) for _ in range(half + 1)] for _ in range(N + 1)]

    states = []
    term = []
    nonterm = 0

    for s in range(1, N + 1):
        for e in range(half + 1):
            m = mask0[s][e]
            while m:
                lsb = m & -m
                a = lsb.bit_length() - 1
                m ^= lsb
                idx = len(states)
                idx0[s][e][a] = idx
                states.append((s, e, 0, a))
                if s == N:
                    if e == half:
                        term.append(idx)
                else:
                    nonterm += 1

            m = mask1[s][e]
            while m:
                lsb = m & -m
                a = lsb.bit_length() - 1
                m ^= lsb
                idx = len(states)
                idx1[s][e][a] = idx
                states.append((s, e, 1, a))
                if s == N:
                    if e == half:
                        term.append(idx)
                else:
                    nonterm += 1

    S = len(states)
    start = idx0[1][1][1]

    trans = [[] for _ in range(S)]
    for idx, (s, e, p, a) in enumerate(states):
        if s == N:
            continue
        r = N - s
        d = half - e

        if p == 0:
            if d == 0:
                bstart = bend = r
            elif 0 < d < r:
                bstart = 1
                bend = r - d
            else:
                continue
        else:
            if d == r:
                bstart = bend = r
            elif 0 < d < r:
                bstart = 1
                bend = d
            else:
                continue

        ab_base = a * stride
        if p == 0:
            for b in range(bstart, bend + 1):
                to = idx1[s + b][e][b]
                if to != -1:
                    trans[idx].append((to, ab_base + b))
        else:
            for b in range(bstart, bend + 1):
                to = idx0[s + b][e + b][b]
                if to != -1:
                    trans[idx].append((to, ab_base + b))

    trans = [tuple(lst) for lst in trans]
    term = tuple(term)

    del states, idx0, idx1, mask0, mask1

    C2 = [0] * (N + 1)
    for b in range(1, N + 1):
        C2[b] = b * (b - 1) // 2
    maxC = C2[N - 1]

    inv = [0] * D
    if D > 1:
        inv[1] = 1
        for i in range(2, D):
            inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    weights = []

    # t = 0: use the removable limit a^b.
    w0 = [0] * A
    for a in range(1, N):
        pwr = 1
        base = a % MOD
        ab_base = a * stride
        for b in range(1, N):
            pwr = pwr * base % MOD
            w0[ab_base + b] = invfact[b] * pwr % MOD
    weights.append(w0)

    # t > 0.
    for t in range(1, D):
        x = (1 + t) % MOD
        pow_x = [1] * (maxC + 1)
        for i in range(1, maxC + 1):
            pow_x[i] = pow_x[i - 1] * x % MOD

        factor = [0] * N
        for b in range(1, N):
            factor[b] = invfact[b] * pow_x[C2[b]] % MOD

        inv_t = inv[t]
        w = [0] * A
        for a in range(1, N):
            base = (pow_x[a] - 1) * inv_t % MOD
            base_pow = 1
            ab_base = a * stride
            for b in range(1, N):
                base_pow = base_pow * base % MOD
                w[ab_base + b] = factor[b] * base_pow % MOD
        weights.append(w)

    weights = tuple(weights)

    y = [0] * D
    mod = MOD
    nonterm_range = range(nonterm)
    trans_local = trans

    for t in range(D):
        wlist = weights[t]
        dp = [0] * S
        dp[start] = 1
        dp_local = dp

        for idx in nonterm_range:
            val = dp_local[idx]
            if val:
                if val >= mod:
                    val %= mod
                if val:
                    for to, ab in trans_local[idx]:
                        dp_local[to] += val * wlist[ab]

        total = 0
        for idx in term:
            total += dp_local[idx]
        y[t] = total % mod

    # Newton forward differences: y(x) = sum d[k] * C(x, k).
    diff = y[:]
    d = [0] * D
    for k in range(D):
        d[k] = diff[0]
        for i in range(D - k - 1):
            diff[i] = (diff[i + 1] - diff[i]) % mod

    # Convert binomial basis C(x,k) to monomial basis using signed Stirling
    # numbers of the first kind.
    c = [0] * D
    if d[0]:
        c[0] = d[0]

    row = [0] * D
    row[0] = 1
    for k in range(1, D):
        nm1 = k - 1
        for j in range(k, 0, -1):
            row[j] = (row[j - 1] - nm1 * row[j]) % mod
        row[0] = 0

        dk = d[k]
        if dk:
            coeff = dk * invfact[k] % mod
            for j in range(1, k + 1):
                c[j] = (c[j] + coeff * row[j]) % mod

    factN1 = fact[N - 1]
    if factN1 != 1:
        for i in range(D):
            c[i] = c[i] * factN1 % mod

    sys.stdout.write(' '.join(str(x % mod) for x in c) + '\n')


if __name__ == '__main__':
    solve()