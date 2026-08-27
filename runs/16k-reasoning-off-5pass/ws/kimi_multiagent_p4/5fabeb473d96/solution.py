import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it)); Q = int(next(it))
    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = int(next(it)) % MOD

    # modular inverses of 1..N+1
    inv = [0] * (N + 2)
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # S1[t] = sum_{i=2..t} A_i / i
    # S2[t] = sum_{i=2..t} 2*A_i*(i-1) / (i*(i+1))
    S1 = [0] * (N + 1)
    S2 = [0] * (N + 1)
    for i in range(2, N + 1):
        S1[i] = (S1[i-1] + A[i] * inv[i]) % MOD
        S2[i] = (S2[i-1] + A[i] * 2 % MOD * (i - 1) % MOD * inv[i] % MOD * inv[i+1]) % MOD

    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD  # (N-1)!

    out = []
    for _ in range(Q):
        u = int(next(it)); v = int(next(it))
        # sum_{i=u+1}^{v-1} A_i / i
        res = (S1[v-1] - S1[u]) % MOD
        # i = v term: A_v * 1
        res = (res + A[v]) % MOD
        if u >= 2:
            # i = u term: A_u * (u-1)/u
            res = (res + A[u] * (u - 1) % MOD * inv[u]) % MOD
            # 2 <= i < u terms
            res = (res + S2[u-1]) % MOD
        out.append(str(res * fact % MOD))
    sys.stdout.write("\n".join(out) + "\n")

main()