import sys

MOD = 998244353


def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])

    # c[l] = count of numbers in [1, N] having l digits
    # S[l] = sum of those numbers modulo MOD
    c = [0] * 7
    S = [0] * 7

    lo = 1
    ten_pow = 10
    for l in range(1, 7):
        hi = ten_pow - 1
        if lo > N:
            break
        if N < hi:
            hi = N
        cnt = hi - lo + 1
        c[l] = cnt
        S[l] = ((lo + hi) * cnt // 2) % MOD
        lo = ten_pow
        ten_pow *= 10

    w = [0] * 7
    for l in range(1, 7):
        w[l] = pow(10, l, MOD)

    # D(t) = product_{l=1..6} (1 + w_l t)
    d = [1]
    for l in range(1, 7):
        wl = w[l]
        new = [0] * (len(d) + 1)
        for i, val in enumerate(d):
            new[i] = (new[i] + val) % MOD
            new[i + 1] = (new[i + 1] + val * wl) % MOD
        d = new

    # R(t) = sum_l c_l w_l * product_{m != l} (1 + w_m t)
    r = [0] * 6
    for l in range(1, 7):
        if c[l] == 0:
            continue

        coef = [1]
        for m in range(1, 7):
            if m == l:
                continue
            wm = w[m]
            new = [0] * (len(coef) + 1)
            for i, val in enumerate(coef):
                new[i] = (new[i] + val) % MOD
                new[i + 1] = (new[i + 1] + val * wm) % MOD
            coef = new

        factor = (c[l] % MOD) * w[l] % MOD
        for i, val in enumerate(coef):
            r[i] = (r[i] + factor * val) % MOD

    # factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD

    # modular inverses of 1..N
    inv = [0] * (N + 1)
    if N >= 1:
        inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # p[k] = coefficient of t^k in W(t) = prod_l (1 + w_l t)^{c_l}
    p = [0] * (N + 1)
    p[0] = 1

    len_d = len(d)
    len_r = len(r)

    for n in range(N):
        val = 0

        upper = len_r - 1
        if upper > n:
            upper = n
        for i in range(upper + 1):
            val += r[i] * p[n - i]

        upper = len_d - 1
        if upper > n + 1:
            upper = n + 1
        for i in range(1, upper + 1):
            val -= d[i] * (n - i + 1) * p[n - i + 1]

        val %= MOD
        p[n + 1] = val * inv[n + 1] % MOD

    ans = 0

    for length in range(1, 7):
        if c[length] == 0:
            continue

        wd = w[length]
        q_prev = 0
        C = 0

        # Q(t) = W(t) / (1 + w_d t)
        for k in range(N):
            q = (p[k] - wd * q_prev) % MOD
            C = (C + q * fact[k] % MOD * fact[N - 1 - k]) % MOD
            q_prev = q

        ans = (ans + C * S[length]) % MOD

    print(ans % MOD)


if __name__ == "__main__":
    main()