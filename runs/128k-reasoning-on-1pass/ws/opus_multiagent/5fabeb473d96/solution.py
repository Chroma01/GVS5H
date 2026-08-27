import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    N = int(data[0]); Q = int(data[1])
    A = data[2:2 + N - 1]

    # modular inverses 1..N+1
    inv = [0] * (N + 2)
    if N + 1 >= 1:
        inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    # (N-1)! mod MOD
    fact = 1
    for i in range(1, N):
        fact = fact * i % MOD

    D = [0] * (N + 1)
    L = [0] * (N + 1)
    s1 = 0  # sum_{i=2}^{x-1} A_i * inv(i)
    s2 = 0  # sum_{i=2}^{x-1} 2*A_i * inv(i)*inv(i+1)
    for x in range(2, N + 1):
        a = int(A[x - 2]) % MOD
        ix = inv[x]
        aix = a * ix % MOD
        D[x] = (a + s1) % MOD
        L[x] = (aix + s2) % MOD
        s1 = (s1 + aix) % MOD
        s2 = (s2 + 2 * aix % MOD * inv[x + 1]) % MOD

    out = []
    idx = 2 + N - 1
    for _ in range(Q):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        if u > v:
            u, v = v, u
        val = (D[u] + D[v] - 2 * L[u]) % MOD
        out.append(fact * val % MOD)

    sys.stdout.write('\n'.join(map(str, out)))

main()