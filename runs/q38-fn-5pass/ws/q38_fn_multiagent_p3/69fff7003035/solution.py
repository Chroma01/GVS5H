import sys

def solve():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])

    maxD = len(str(N))

    cnt = [0] * (maxD + 1)
    sumv = [0] * (maxD + 1)
    qs = [0] * (maxD + 1)
    lengths = []

    q = 1
    for d in range(1, maxD + 1):
        q = (q * 10) % MOD
        qs[d] = q

    start = 1
    for d in range(1, maxD + 1):
        end = min(N, start * 10 - 1)
        if start <= N:
            c = end - start + 1
            cnt[d] = c
            sumv[d] = ((start + end) * c // 2) % MOD
            lengths.append(d)
        start *= 10

    D = len(lengths)

    # Q(z) = product over digit lengths d of (1 + q_d z)
    Q = [1] + [0] * D
    deg = 0
    for d in lengths:
        q = qs[d]
        for i in range(deg, -1, -1):
            Q[i + 1] = (Q[i + 1] + Q[i] * q) % MOD
        deg += 1

    # R(z) = sum_d cnt_d * q_d * Q(z) / (1 + q_d z)
    R = [0] * D
    for d in lengths:
        q = qs[d]
        cq = (cnt[d] * q) % MOD
        h = 1
        R[0] = (R[0] + cq) % MOD
        for i in range(1, D):
            h = (Q[i] - q * h) % MOD
            R[i] = (R[i] + cq * h) % MOD

    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv = [0] * (N + 1)
    if N >= 1:
        inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # P(z) = product_d (1 + q_d z)^cnt_d
    # Coefficients p[k] via Q P' = R P.
    p = [0] * (N + 1)
    p[0] = 1

    for n in range(1, N + 1):
        m = D if D < n else n
        s = 0
        for i in range(m):
            s += R[i] * p[n - 1 - i]
        s %= MOD

        m = D if D < n else n - 1
        t = 0
        for i in range(1, m + 1):
            t += Q[i] * (n - i) * p[n - i]
        t %= MOD

        p[n] = (s - t) * inv[n] % MOD

    Nm1 = N - 1
    weight = [fact[k] * fact[Nm1 - k] % MOD for k in range(N)]

    ans = 0

    # For each digit length d, divide P by (1 + q_d z) and accumulate.
    for d in lengths:
        q = qs[d]
        e = 1
        total = weight[0]

        for k in range(1, N):
            e = (p[k] - q * e) % MOD
            total += weight[k] * e

        total %= MOD
        ans = (ans + sumv[d] * total) % MOD

    print(ans)

if __name__ == "__main__":
    solve()