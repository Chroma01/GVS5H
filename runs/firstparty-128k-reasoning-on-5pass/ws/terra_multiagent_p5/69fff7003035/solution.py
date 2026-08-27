import sys

MOD = 998244353


def main():
    N = int(sys.stdin.readline())

    max_d = len(str(N))
    groups = []

    for d in range(1, max_d + 1):
        lo = 10 ** (d - 1)
        hi = min(N, 10 ** d - 1)
        if lo > hi:
            continue
        count = hi - lo + 1
        value_sum = (lo + hi) * count // 2 % MOD
        a = pow(10, d, MOD)
        groups.append((a, count, value_sum))

    D = len(groups)

    # Q(z) = product (1 + a_d z), with one factor per digit-length class.
    Q = [1]
    for a, _, _ in groups:
        Q.append(0)
        for j in range(len(Q) - 1, 0, -1):
            Q[j] = (Q[j] + a * Q[j - 1]) % MOD

    # P(z) = sum_d c_d * a_d * product_{e != d}(1 + a_e z).
    # This satisfies Q(z) F'(z) = P(z) F(z), where
    # F(z) = product_d (1 + a_d z)^{c_d}.
    P = [0] * D
    for a, count, _ in groups:
        other = [0] * D
        other[0] = 1
        for j in range(1, D):
            other[j] = (Q[j] - a * other[j - 1]) % MOD
        factor = (count % MOD) * a % MOD
        for j in range(D):
            P[j] = (P[j] + factor * other[j]) % MOD

    inv = [0] * (N + 1)
    if N >= 1:
        inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # Coefficients of F(z), up to degree N.
    F = [0] * (N + 1)
    F[0] = 1

    for n in range(1, N + 1):
        rhs = 0
        upper_p = min(D - 1, n - 1)
        for j in range(upper_p + 1):
            rhs += P[j] * F[n - 1 - j]

        lhs_extra = 0
        upper_q = min(D, n - 1)
        for j in range(1, upper_q + 1):
            lhs_extra += Q[j] * (n - j) * F[n - j]

        F[n] = (rhs - lhs_extra) % MOD * inv[n] % MOD

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD

    answer = 0

    for a, _, value_sum in groups:
        # G(z) = F(z) / (1 + a z), corresponding to excluding one
        # particular value in this digit-length class.
        G_prev = 1
        multiplier = fact[N - 1]  # k = 0 term: 0! * (N-1)! * G[0]

        for k in range(1, N):
            G_cur = (F[k] - a * G_prev) % MOD
            multiplier = (multiplier + fact[k] * fact[N - 1 - k] % MOD * G_cur) % MOD
            G_prev = G_cur

        answer = (answer + value_sum * multiplier) % MOD

    print(answer)


if __name__ == "__main__":
    main()