import sys

MOD = 998244353

def multiply_linear(poly, a, b):
    res = [0] * (len(poly) + 1)
    for i, v in enumerate(poly):
        res[i] = (res[i] + v * a) % MOD
        res[i + 1] = (res[i + 1] + v * b) % MOD
    return res

def main():
    N = int(sys.stdin.readline())

    max_d = len(str(N))
    cnt = [0] * (max_d + 1)
    val_sum = [0] * (max_d + 1)

    for x in range(1, N + 1):
        d = len(str(x))
        cnt[d] += 1
        val_sum[d] += x

    pow10 = [1] * (max_d + 1)
    for d in range(1, max_d + 1):
        pow10[d] = pow10[d - 1] * 10 % MOD

    # L_d(t) = 10^d + (1 - 10^d)t.
    # D(t) = product of the distinct L_d(t).
    D = [1]
    a = [0] * (max_d + 1)
    b = [0] * (max_d + 1)
    for d in range(1, max_d + 1):
        a[d] = pow10[d]
        b[d] = (1 - a[d]) % MOD
        D = multiply_linear(D, a[d], b[d])

    # E(t) = sum_d cnt[d] * b[d] * product_{e != d} L_e(t).
    E = [0] * max_d
    for d in range(1, max_d + 1):
        if cnt[d] == 0:
            continue
        other = [1]
        for e in range(1, max_d + 1):
            if e != d:
                other = multiply_linear(other, a[e], b[e])
        scale = cnt[d] * b[d] % MOD
        for i, v in enumerate(other):
            E[i] = (E[i] + scale * v) % MOD

    # P(t) = product_d L_d(t)^cnt[d].
    # From D(t)P'(t)=E(t)P(t), compute all coefficients in O(max_d*N).
    P = [0] * (N + 1)
    p0 = 1
    for d in range(1, max_d + 1):
        p0 = p0 * pow(a[d], cnt[d], MOD) % MOD
    P[0] = p0

    inv_d0 = pow(D[0], MOD - 2, MOD)
    deg_d = len(D) - 1
    deg_e = len(E) - 1

    for k in range(N):
        rhs = 0
        for i in range(min(deg_e, k) + 1):
            rhs += E[i] * P[k - i]
        rhs %= MOD

        known = 0
        for i in range(1, min(deg_d, k) + 1):
            known += D[i] * (k - i + 1) * P[k - i + 1]
        known %= MOD

        P[k + 1] = (rhs - known) % MOD
        P[k + 1] = P[k + 1] * pow(k + 1, MOD - 2, MOD) % MOD
        P[k + 1] = P[k + 1] * inv_d0 % MOD

    inv = [0] * (N + 1)
    if N >= 1:
        inv[1] = 1
        for i in range(2, N + 1):
            inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    total_expectation = 0

    # For each digit length d, divide P by L_d.
    # This gives the polynomial for all elements except a fixed d-digit element.
    for d in range(1, max_d + 1):
        if cnt[d] == 0:
            continue

        quotient = [0] * N
        inv_a = pow(a[d], MOD - 2, MOD)
        quotient[0] = P[0] * inv_a % MOD
        for i in range(1, N):
            quotient[i] = (P[i] - b[d] * quotient[i - 1]) % MOD
            quotient[i] = quotient[i] * inv_a % MOD

        integral = 0
        for i, coef in enumerate(quotient):
            integral += coef * inv[i + 1]
        integral %= MOD

        total_expectation = (total_expectation + (val_sum[d] % MOD) * integral) % MOD

    fact = 1
    for i in range(2, N + 1):
        fact = fact * i % MOD

    print(total_expectation * fact % MOD)

if __name__ == "__main__":
    main()