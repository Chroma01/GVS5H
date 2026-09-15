import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    P = int(data[1])
    H = N // 2
    D = N * (N - 1) // 2

    # factorials up to D
    fact = [1] * (D + 1)
    for i in range(1, D + 1):
        fact[i] = fact[i-1] * i % P
    invfact = [1] * (D + 1)
    invfact[D] = pow(fact[D], P - 2, P)
    for i in range(D, 0, -1):
        invfact[i-1] = invfact[i] * i % P

    def C(n, k):
        if k < 0 or k > n:
            return 0
        return fact[n] * invfact[k] % P * invfact[n-k] % P

    # index for DP state (E, O, s, p)
    def idx(E, O, s, p):
        return ((E * (H + 1) + O) * (N + 1) + s) * 2 + p

    S = (H + 1) * (H + 1) * (N + 1) * 2

    # precompute all valid transitions grouped by total used vertices t
    states_by_t = [[] for _ in range(N)]  # t = 1 .. N-1
    for t in range(1, N):
        E_start = max(0, t - H)
        E_end = min(H, t)
        for E in range(E_start, E_end + 1):
            O = t - E
            for s in range(1, t + 1):
                for p in (0, 1):
                    if p == 0 and s > E:
                        continue
                    if p == 1 and s > O:
                        continue
                    state_idx = idx(E, O, s, p)
                    q = 1 - p
                    if q == 1:
                        rem = H - O
                    else:
                        rem = H - E
                    if rem == 0:
                        continue
                    trans = []
                    for b in range(1, rem + 1):
                        newE = E + (b if q == 0 else 0)
                        newO = O + (b if q == 1 else 0)
                        newS = b
                        newP = q
                        new_idx = idx(newE, newO, newS, newP)
                        c = C(rem, b)
                        trans.append((new_idx, c, b, s))
                    if trans:
                        states_by_t[t].append((state_idx, trans))

    # small binomial coefficients for cover computation
    comb_small = [[0] * (N + 1) for _ in range(N + 1)]
    for b in range(N + 1):
        for i in range(b + 1):
            comb_small[b][i] = C(b, i)

    y = [0] * (D + 1)
    start_idx = idx(1, 0, 1, 0)
    final_indices = [idx(H, H, s, p) for s in range(1, N + 1) for p in (0, 1)]

    for x in range(D + 1):
        base = (1 + x) % P
        w = [1] * (D + 1)
        wk = 1
        for k in range(1, D + 1):
            wk = wk * base % P
            w[k] = wk

        I = [1] * (N + 1)
        for b in range(2, N + 1):
            I[b] = w[b * (b - 1) // 2]

        # cover_w[s][b] = (number of ways to connect level of size s to size b covering all b) * (1+x)^{C(b,2)}
        cover_w = [[0] * (N + 1) for _ in range(N + 1)]
        for s in range(1, N + 1):
            for b in range(1, N - s + 1):
                total = 0
                for i in range(b + 1):
                    term = comb_small[b][i] * w[s * i] % P
                    if (b - i) & 1:
                        total -= term
                    else:
                        total += term
                cover_w[s][b] = (total % P) * I[b] % P

        dp = [0] * S
        dp[start_idx] = 1
        for t in range(1, N):
            for state_idx, trans in states_by_t[t]:
                val = dp[state_idx]
                if val == 0:
                    continue
                for new_idx, c, b, s in trans:
                    wgt = c * cover_w[s][b] % P
                    dp[new_idx] = (dp[new_idx] + val * wgt) % P

        res = 0
        for fi in final_indices:
            res += dp[fi]
        y[x] = res % P

    # Lagrange interpolation to recover coefficients a[0..D]
    poly = [1]
    for j in range(D + 1):
        new_poly = [0] * (len(poly) + 1)
        for i, coeff in enumerate(poly):
            new_poly[i] = (new_poly[i] - j * coeff) % P
            new_poly[i + 1] = (new_poly[i + 1] + coeff) % P
        poly = new_poly

    a = [0] * (D + 1)
    for i in range(D + 1):
        Q = [0] * (D + 1)
        Q[D] = 1
        for k in range(D, 0, -1):
            Q[k - 1] = (poly[k] + i * Q[k]) % P
        denom = fact[i] * fact[D - i] % P
        if (D - i) & 1:
            denom = (-denom) % P
        inv_denom = pow(denom, P - 2, P)
        factor = y[i] * inv_denom % P
        for k in range(D + 1):
            a[k] = (a[k] + factor * Q[k]) % P

    comb_part = C(N - 1, H)
    out = []
    for M in range(N - 1, D + 1):
        out.append(str(a[M] * comb_part % P))
    print(" ".join(out))

if __name__ == "__main__":
    main()