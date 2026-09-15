import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    P = int(data[1])
    half = N // 2
    maxE = N * (N - 1) // 2

    # Binomial coefficients up to maxE
    binom = [[1]]
    for e in range(1, maxE + 1):
        prev = binom[-1]
        row = [1] * (e + 1)
        for k in range(1, e):
            row[k] = (prev[k-1] + prev[k]) % P
        binom.append(row)

    # G[s][t] = (1+x)^{C(t,2)} * sum_j (-1)^j C(t,j) (1+x)^{s(t-j)}
    G = [[None] * (N + 1) for _ in range(N + 1)]
    for s in range(1, N + 1):
        for t in range(1, N + 1 - s):
            maxdeg = t * (t - 1) // 2 + s * t
            poly = [0] * (maxdeg + 1)
            for j in range(t + 1):
                coef = binom[t][j]
                e = t * (t - 1) // 2 + s * (t - j)
                row = binom[e]
                if (j & 1) == 0:
                    for k, val in enumerate(row):
                        poly[k] += coef * val
                else:
                    for k, val in enumerate(row):
                        poly[k] -= coef * val
            for k in range(len(poly)):
                poly[k] %= P
            G[s][t] = poly

    SHIFT = 72
    MASK = (1 << SHIFT) - 1

    def pack_scaled(p, scalar):
        A = 0
        if scalar == 1:
            for x in reversed(p):
                A = (A << SHIFT) | x
        else:
            for x in reversed(p):
                A = (A << SHIFT) | ((x * scalar) % P)
        return A

    dp = [dict() for _ in range(N + 1)]
    dp[1][(1, 1, 0)] = [1]

    for placed in range(1, N):
        cur = dp[placed]
        if not cur:
            continue
        for key in cur:
            poly = cur[key]
            cur[key] = [x % P for x in poly]

        remaining = N - placed
        for (last, even, parity), poly in cur.items():
            odd = placed - even
            packed_poly = pack_scaled(poly, 1)
            for t in range(1, remaining + 1):
                new_parity = 1 - parity
                if new_parity == 0:
                    new_even = even + t
                    new_odd = odd
                else:
                    new_even = even
                    new_odd = odd + t
                if new_even > half or new_odd > half:
                    continue
                new_placed = placed + t
                scalar = binom[remaining][t]
                if scalar == 0:
                    continue
                factor = G[last][t]
                need = len(poly) + len(factor) - 1
                key_new = (t, new_even, new_parity)
                target = dp[new_placed]
                packed_sf = pack_scaled(factor, scalar)

                if key_new in target:
                    existing = target[key_new]
                    if len(existing) < need:
                        existing.extend([0] * (need - len(existing)))
                    C = packed_poly * packed_sf
                    for i in range(need):
                        existing[i] += C & MASK
                        C >>= SHIFT
                else:
                    new_poly = [0] * need
                    C = packed_poly * packed_sf
                    for i in range(need):
                        new_poly[i] = C & MASK
                        C >>= SHIFT
                    target[key_new] = new_poly

    ans = [0] * (maxE + 1)
    for (last, even, parity), poly in dp[N].items():
        if even == half:
            for i, val in enumerate(poly):
                if i <= maxE:
                    ans[i] = (ans[i] + val) % P

    out = [str(ans[M] % P) for M in range(N - 1, maxE + 1)]
    sys.stdout.write(' '.join(out))

if __name__ == '__main__':
    solve()