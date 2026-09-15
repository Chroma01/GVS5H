import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    Q = int(data[pos]); pos += 1
    MOD = 998244353

    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = int(data[pos]); pos += 1

    # modular inverses 1..N+1
    maxn = N + 1
    inv = [0] * (maxn + 2)
    inv[1] = 1
    for i in range(2, maxn + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    # prefix sums
    S1 = [0] * (N + 1)   # S1[i] = sum_{j=2..i} A_j / j
    S2 = [0] * (N + 1)   # S2[i] = sum_{j=2..i} 2(j-1) A_j / (j(j+1))
    for i in range(2, N + 1):
        S1[i] = (S1[i - 1] + A[i] * inv[i]) % MOD
        S2[i] = (S2[i - 1] + 2 * (i - 1) % MOD * A[i] % MOD
                 * inv[i] % MOD * inv[i + 1]) % MOD

    # (N-1)!
    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD

    out = []
    for _ in range(Q):
        u = int(data[pos]); pos += 1
        v = int(data[pos]); pos += 1
        # E = expected distance in uniformly random recursive tree
        E = (S2[u - 1]
             + A[u] * (u - 1) % MOD * inv[u]
             + S1[v - 1] - S1[u]
             + A[v]) % MOD
        out.append(E * fact % MOD)

    sys.stdout.write('\n'.join(map(str, out)))
    sys.stdout.write('\n')

main()