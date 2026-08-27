import sys

def solve():
    MOD = 998244353
    input = sys.stdin.readline
    N, Q = map(int, input().split())
    A = [0] * (N + 1)
    A[2:] = list(map(int, input().split()))

    # Precompute factorials and inverse factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i-1] * i % MOD
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD-2, MOD)
    for i in range(N, 0, -1):
        inv_fact[i-1] = inv_fact[i] * i % MOD
    inv = [0] * (N + 1)
    for i in range(1, N + 1):
        inv[i] = inv_fact[i] * fact[i-1] % MOD

    F = fact[N-1]  # (N-1)!
    inv_F = inv_fact[N-1]

    # Compute T[i] for i = 2..N-2: number of trees where i is ancestor of both u,v (for any u,v > i)
    T = [0] * (N + 1)
    # For i <= N-4, use closed form: T(i) = (N-1)! * 2 / (i(i-1)(i+1))
    for i in range(2, N-3):
        T[i] = F * 2 % MOD
        T[i] = T[i] * inv[i] % MOD
        T[i] = T[i] * inv[i-1] % MOD
        T[i] = T[i] * inv[i+1] % MOD
    # For i = N-4, N-3, N-2, compute directly using combinatorial sum
    for i in range(max(2, N-4), N-1):
        M = N - i
        if M < 2:
            T[i] = 0
            continue
        total = 0
        for k in range(2, M+1):
            binom = fact[M-2] * inv_fact[k-2] % MOD * inv_fact[M-k] % MOD
            term = binom * fact[k] % MOD * fact[N-k-2] % MOD
            total = (total + term) % MOD
        T[i] = (i-1) * total % MOD
    T[N-1] = 0
    T[N] = 0

    # f[i] = T[i] / F
    f = [0] * (N + 1)
    for i in range(2, N+1):
        f[i] = T[i] * inv_F % MOD

    # Prefix sums: pre1[i] = sum_{j=2..i} A_j / j, pre2[i] = sum_{j=2..i} A_j * f[j]
    pre1 = [0] * (N + 1)
    pre2 = [0] * (N + 1)
    for i in range(2, N+1):
        pre1[i] = (pre1[i-1] + A[i] * inv[i]) % MOD
        pre2[i] = (pre2[i-1] + A[i] * f[i]) % MOD

    out = []
    for _ in range(Q):
        u, v = map(int, input().split())
        if u > v:
            u, v = v, u
        if u == 1:
            ans = F * (pre1[v] - pre1[1]) % MOD
        else:
            part1 = 2 * (pre1[u-1] - pre1[1]) % MOD
            part2 = 2 * (pre2[u-1] - pre2[1]) % MOD
            part3 = A[u] * (1 - 2 * inv[v]) % MOD
            part4 = (pre1[v-1] - pre1[u]) % MOD
            part5 = A[v]
            total = (part1 - part2 + part3 + part4 + part5) % MOD
            ans = F * total % MOD
        out.append(ans % MOD)

    print('\n'.join(map(str, out)))

solve()