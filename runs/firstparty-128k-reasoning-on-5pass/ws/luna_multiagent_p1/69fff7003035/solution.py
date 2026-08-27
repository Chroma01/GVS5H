import sys

MOD = 998244353


def solve():
    n = int(sys.stdin.readline())

    counts = [0] * 7
    sums = [0] * 7

    for x in range(1, n + 1):
        d = len(str(x))
        counts[d] += 1
        sums[d] += x

    # H(z) = product over present digit lengths d of (1 + 10^d z)
    # R(z) = sum_d c_d * 10^d * H(z)/(1 + 10^d z)
    H = [1]
    present = []

    for d in range(1, 7):
        if counts[d]:
            present.append(d)
            w = pow(10, d, MOD)
            new_h = [0] * (len(H) + 1)
            for i, value in enumerate(H):
                new_h[i] = (new_h[i] + value) % MOD
                new_h[i + 1] = (new_h[i + 1] + value * w) % MOD
            H = new_h

    degree_h = len(H) - 1
    R = [0] * degree_h

    for d in present:
        w = pow(10, d, MOD)

        # Quotient Q = H / (1 + w z)
        quotient = [0] * degree_h
        quotient[0] = H[0]
        for i in range(1, degree_h):
            quotient[i] = (H[i] - w * quotient[i - 1]) % MOD

        multiplier = counts[d] * w % MOD
        for i in range(degree_h):
            R[i] = (R[i] + multiplier * quotient[i]) % MOD

    # Coefficients of G(z) = product_d (1 + 10^d z)^{c_d}
    # are obtained from H(z)G'(z) = R(z)G(z).
    inv = [0] * (n + 1)
    inv[1] = 1
    for i in range(2, n + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    g = [0] * (n + 1)
    g[0] = 1

    for k in range(1, n + 1):
        rhs = 0
        max_r = min(degree_h - 1, k - 1)
        for i in range(max_r + 1):
            rhs += R[i] * g[k - 1 - i]

        subtract = 0
        max_h = min(degree_h, k - 1)
        for i in range(1, max_h + 1):
            subtract += H[i] * (k - i) * g[k - i]

        g[k] = (rhs - subtract) % MOD
        g[k] = g[k] * inv[k] % MOD

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    answer = 0

    for d in present:
        w = pow(10, d, MOD)

        # Coefficients after excluding one element of digit length d.
        q = [0] * n
        q[0] = g[0]
        for k in range(1, n):
            q[k] = (g[k] - w * q[k - 1]) % MOD

        positional_weight = 0
        for k in range(n):
            positional_weight += q[k] * fact[k] % MOD * fact[n - 1 - k]
        positional_weight %= MOD

        answer = (answer + (sums[d] % MOD) * positional_weight) % MOD

    print(answer)


if __name__ == "__main__":
    solve()