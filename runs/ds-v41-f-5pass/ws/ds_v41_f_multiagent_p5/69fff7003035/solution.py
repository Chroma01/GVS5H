import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    MOD = 998244353

    # factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD

    # modular inverses 1..N
    inv = [0] * (N + 1)
    inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    # count c[d] and sum S[d] of integers in 1..N having digit length d
    c = [0] * 7
    S = [0] * 7
    pw = 1
    for d in range(1, 7):
        lo = pw
        pw *= 10
        hi = min(N, pw - 1)
        if lo > hi:
            break
        cnt = hi - lo + 1
        c[d] = cnt
        S[d] = ((lo + hi) * cnt // 2) % MOD

    present = [d for d in range(1, 7) if c[d] > 0]
    ad = []
    # F(z) = prod_{d present} (1 + 10^d z),  deg <= 6
    F = [1]
    for d in present:
        a = pow(10, d, MOD)
        ad.append((d, a))
        nf = [0] * (len(F) + 1)
        for j in range(len(F)):
            coef = F[j]
            nf[j] = (nf[j] + coef) % MOD
            nf[j + 1] = (nf[j + 1] + coef * a) % MOD
        F = nf
    t = len(F) - 1

    # G(z) = sum_d c_d * 10^d * F(z)/(1+10^d z),  deg <= 5
    G = [0] * t
    for d, a in ad:
        ca = c[d] * a % MOD
        Hprev = 1
        G[0] = (G[0] + ca) % MOD
        for j in range(1, t):
            Hj = (F[j] - a * Hprev) % MOD
            G[j] = (G[j] + ca * Hj) % MOD
            Hprev = Hj

    # Q(z) = prod (1+10^d z)^{c_d} via D*Q' = P*Q recurrence
    q = [0] * (N + 1)
    q[0] = 1
    lf = len(F)
    lg = len(G)
    for n in range(1, N + 1):
        s = 0
        jm = lg - 1
        if jm > n - 1:
            jm = n - 1
        for j in range(jm + 1):
            s += G[j] * q[n - 1 - j]
        jm2 = lf - 1
        if jm2 > n:
            jm2 = n
        for j in range(1, jm2 + 1):
            s -= F[j] * (n - j) * q[n - j]
        q[n] = (s % MOD) * inv[n] % MOD

    # weights m!*(N-1-m)!
    warr = [0] * (N + 1)
    for m in range(N):
        warr[m] = fact[m] * fact[N - 1 - m] % MOD

    ans = 0
    for d, a in ad:
        # R(z) = Q(z)/(1+10^d z):  R_m = q_m - a*R_{m-1}, R_0 = 1
        R = 1
        E = warr[0]
        for m in range(1, N):
            R = (q[m] - a * R) % MOD
            E += R * warr[m]
        E %= MOD
        ans = (ans + S[d] * E) % MOD

    print(ans % MOD)

main()