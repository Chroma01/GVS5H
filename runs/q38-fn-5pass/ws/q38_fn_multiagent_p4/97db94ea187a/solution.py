import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    P = int(data[1])

    H = N // 2
    E = N * (N - 1) // 2

    # Binomial coefficients modulo P.
    comb = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        comb[i][0] = comb[i][i] = 1
        for j in range(1, i):
            comb[i][j] = (comb[i - 1][j - 1] + comb[i - 1][j]) % P

    C2 = [i * (i - 1) // 2 for i in range(N + 1)]
    stride = N + 1

    # State: (even_count, odd_count, last_layer_size, last_layer_parity)
    # parity 0 = even layer, 1 = odd layer.  Root is layer 0.
    start = (1, 0, 1, 0)
    states = [start]
    idx_map = {start: 0}
    trans = [[]]

    head = 0
    while head < len(states):
        e, o, p, par = states[head]
        u = e + o

        if u < N:
            if par == 0:
                maxa = H - o
                newpar = 1
            else:
                maxa = H - e
                newpar = 0

            rem = N - u
            for a in range(1, maxa + 1):
                if newpar == 1:
                    ne, no = e, o + a
                else:
                    ne, no = e + a, o

                # If the next parity is already full but vertices remain,
                # this partial layer sequence can never finish.
                if ne + no < N:
                    if (newpar == 0 and no == H) or (newpar == 1 and ne == H):
                        continue

                key = (ne, no, a, newpar)
                nidx = idx_map.get(key)
                if nidx is None:
                    nidx = len(states)
                    idx_map[key] = nidx
                    states.append(key)
                    trans.append([])

                # Label choice: choose a labels from remaining vertices.
                trans[head].append((nidx, p * stride + a, comb[rem][a]))

        head += 1

    trans = [tuple(lst) for lst in trans]

    group = [[] for _ in range(N + 1)]
    final_indices = []
    for i, (e, o, p, par) in enumerate(states):
        u = e + o
        if u == N:
            final_indices.append(i)
        elif trans[i]:
            group[u].append(i)

    group = [tuple(lst) for lst in group]
    final_indices = tuple(final_indices)
    S = len(states)

    del idx_map, states

    # Modular inverses up to E.
    inv = [0] * (E + 1)
    if E >= 1:
        inv[1] = 1
        for i in range(2, E + 1):
            inv[i] = (P - (P // i) * inv[P % i] % P) % P

    # Evaluate the generating polynomial at x = 0, 1, ..., E.
    # F(0) = 0 because N >= 2 and every connected graph has at least N-1 edges.
    y = [0] * (E + 1)

    Pmod = P
    Nmod = N
    stride_local = stride
    C2_local = C2
    trans_local = trans
    group_local = group
    final_local = final_indices
    S_local = S

    for x in range(1, E + 1):
        one = (1 + x) % Pmod

        pow1 = [1] * (E + 1)
        for t in range(1, E + 1):
            pow1[t] = (pow1[t - 1] * one) % Pmod

        powC2 = [pow1[c] for c in C2_local]

        # WA[p, a] = (1+x)^{C(a,2)} * ((1+x)^p - 1)^a
        WA = [0] * ((Nmod + 1) * (Nmod + 1))
        for p in range(1, Nmod + 1):
            base = pow1[p] - 1
            if base < 0:
                base += Pmod
            val = 1
            pa_base = p * stride_local
            for a in range(1, Nmod + 1):
                val = (val * base) % Pmod
                WA[pa_base + a] = (val * powC2[a]) % Pmod

        dp = [0] * S_local
        dp[0] = 1

        for u in range(1, Nmod):
            for idx in group_local[u]:
                val = dp[idx]
                if val:
                    for nidx, pa, base in trans_local[idx]:
                        add = (val * base * WA[pa]) % Pmod
                        nv = dp[nidx] + add
                        if nv >= Pmod:
                            nv -= Pmod
                        dp[nidx] = nv

        total = 0
        for idx in final_local:
            total += dp[idx]
        y[x] = total % Pmod

    # Newton forward differences:
    # F(x) = sum_k diff[k] * binom(x, k)
    d = y[:]
    diff = [0] * (E + 1)
    for k in range(E + 1):
        diff[k] = d[0]
        for i in range(E - k):
            v = d[i + 1] - d[i]
            if v < 0:
                v += Pmod
            d[i] = v

    # Convert from binomial basis to ordinary powers.
    poly = [0] * (E + 1)
    binom = [1]  # binom(x, 0)

    for k in range(E + 1):
        if k > 0:
            new = [0] * (k + 1)
            shift = k - 1

            if shift == 0:
                new[1] = binom[0]
            else:
                for i, c in enumerate(binom):
                    if c:
                        new[i] = (new[i] - c * shift) % Pmod
                        new[i + 1] = (new[i + 1] + c) % Pmod

            invk = inv[k]
            if invk != 1:
                binom = [(c * invk) % Pmod for c in new]
            else:
                binom = new

        ck = diff[k]
        if ck:
            for i, c in enumerate(binom):
                if c:
                    poly[i] = (poly[i] + ck * c) % Pmod

    ans = [str(poly[m]) for m in range(N - 1, E + 1)]
    sys.stdout.write(" ".join(ans) + "\n")


if __name__ == "__main__":
    solve()