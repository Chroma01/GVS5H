import sys

MOD = 998244353


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])

    counts = {}
    sums = {}
    for x in range(1, n + 1):
        d = len(str(x))
        counts[d] = counts.get(d, 0) + 1
        sums[d] = (sums.get(d, 0) + x) % MOD

    digits = sorted(counts)
    m = len(digits)
    qs = [pow(10, d, MOD) for d in digits]
    cs = [counts[d] for d in digits]

    # Q(z) = product_i (1 + q_i z), with one factor per distinct length.
    Q = [1]
    for q in qs:
        new = [0] * (len(Q) + 1)
        for j, val in enumerate(Q):
            new[j] = (new[j] + val) % MOD
            new[j + 1] = (new[j + 1] + val * q) % MOD
        Q = new

    # R(z) = sum_i c_i q_i * product_{j != i} (1 + q_j z).
    R = [0] * m
    for i, (c, q) in enumerate(zip(cs, qs)):
        excl = [1]
        for j, q2 in enumerate(qs):
            if i == j:
                continue
            new = [0] * (len(excl) + 1)
            for t, val in enumerate(excl):
                new[t] = (new[t] + val) % MOD
                new[t + 1] = (new[t + 1] + val * q2) % MOD
            excl = new
        factor = c * q % MOD
        for t, val in enumerate(excl):
            R[t] = (R[t] + factor * val) % MOD

    # Coefficients of G(z) = product_i (1 + q_i z)^{c_i}.
    g = [0] * (n + 1)
    g[0] = 1

    inv = [0] * (n + 1)
    if n >= 1:
        inv[1] = 1
        for i in range(2, n + 1):
            inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    degree_q = len(Q) - 1
    degree_r = len(R) - 1
    for k in range(1, n + 1):
        rhs = 0
        upper = min(degree_r, k - 1)
        for t in range(upper + 1):
            rhs = (rhs + R[t] * g[k - 1 - t]) % MOD

        lhs_other = 0
        upper = min(degree_q, k - 1)
        for t in range(1, upper + 1):
            lhs_other = (
                lhs_other + Q[t] * (k - t) * g[k - t]
            ) % MOD

        g[k] = (rhs - lhs_other) * inv[k] % MOD

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    answer = 0
    for idx, d in enumerate(digits):
        # G(z) = (1 + q z) * F_d(z), where F_d excludes one element
        # from the digit-length class d.
        q = qs[idx]
        f = [0] * n
        f[0] = 1
        for k in range(1, n):
            f[k] = (g[k] - q * f[k - 1]) % MOD

        weighted = 0
        for k in range(n):
            weighted = (
                weighted + f[k] * fact[k] % MOD * fact[n - 1 - k]
            ) % MOD

        answer = (answer + sums[d] * weighted) % MOD

    print(answer)


if __name__ == "__main__":
    solve()