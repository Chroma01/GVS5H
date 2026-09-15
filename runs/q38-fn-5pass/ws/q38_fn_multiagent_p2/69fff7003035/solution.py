import sys

MOD = 998244353


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])

    max_len = len(str(N))

    cnt = [0] * (max_len + 1)
    sum_val = [0] * (max_len + 1)

    start = 1
    for d in range(1, max_len + 1):
        end = min(N, 10 ** d - 1)
        if start <= end:
            c = end - start + 1
            cnt[d] = c
            sum_val[d] = ((start + end) * c // 2) % MOD
        start = 10 ** d

    ds = [d for d in range(1, max_len + 1) if cnt[d] > 0]
    L = len(ds)

    w = [0] * (max_len + 1)
    for d in ds:
        w[d] = pow(10, d, MOD)

    # Q(z) = product_{d in ds} (1 + w_d z)
    q = [1]
    for d in ds:
        wd = w[d]
        new = [0] * (len(q) + 1)
        for i, val in enumerate(q):
            new[i] = (new[i] + val) % MOD
            new[i + 1] = (new[i + 1] + wd * val) % MOD
        q = new

    # R(z) = Q(z) * sum_d c_d w_d / (1 + w_d z)
    #      = sum_d c_d w_d * product_{e != d} (1 + w_e z)
    r = [0] * L
    for d in ds:
        poly = [1]
        for e in ds:
            if e == d:
                continue
            we = w[e]
            new = [0] * (len(poly) + 1)
            for i, val in enumerate(poly):
                new[i] = (new[i] + val) % MOD
                new[i + 1] = (new[i + 1] + we * val) % MOD
            poly = new

        coeff = (cnt[d] % MOD) * w[d] % MOD
        for j, val in enumerate(poly):
            r[j] = (r[j] + coeff * val) % MOD

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv = [0] * (N + 1)
    if N >= 1:
        inv[1] = 1
        for i in range(2, N + 1):
            inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # p[k] = coefficient of z^k in P(z) = product_d (1 + w_d z)^{c_d}
    p = [0] * (N + 1)
    p[0] = 1

    q_list = q
    r_list = r
    inv_list = inv
    p_list = p
    mod = MOD
    L_val = L

    # From Q(z) P'(z) = P(z) R(z), derive coefficients in O(LN).
    for n in range(N):
        rhs = 0

        maxj = L_val - 1
        if maxj > n:
            maxj = n
        for j in range(maxj + 1):
            rhs += r_list[j] * p_list[n - j]

        maxj2 = L_val
        if maxj2 > n:
            maxj2 = n
        for j in range(1, maxj2 + 1):
            rhs -= q_list[j] * (n - j + 1) * p_list[n - j + 1]

        p_list[n + 1] = (rhs % mod) * inv_list[n + 1] % mod

    # Reuse inv[] as weight[k] = k! * (N-1-k)!.
    for k in range(N):
        inv[k] = fact[k] * fact[N - 1 - k] % mod

    weight = inv
    ans = 0

    # For each digit length d, divide P(z) by (1 + w_d z)
    # and apply the factorial weights.
    for d in ds:
        wd = w[d]

        # Quotient coefficient q_0 = 1.
        m = weight[0]
        qcoef = 1

        for k in range(1, N):
            # Synthetic division:
            # p_k = quotient_k + w_d * quotient_{k-1}
            qcoef = (p_list[k] - wd * qcoef) % mod
            m += qcoef * weight[k]

        ans = (ans + (m % mod) * sum_val[d]) % mod

    print(ans)


if __name__ == "__main__":
    solve()