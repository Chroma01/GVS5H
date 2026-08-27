import sys

def solve():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    Q = int(data[pos]); pos += 1
    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = int(data[pos]) % MOD
        pos += 1

    # factorial (N-1)!
    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD

    # modular inverses of 1..N+1
    inv = [0] * (N + 2)
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - MOD // i * inv[MOD % i] % MOD

    # P1[k] = sum_{2<=i<=k} A_i * 2(i-1) / (i(i+1))
    # P2[k] = sum_{2<=i<=k} A_i / i
    P1 = [0] * (N + 1)
    P2 = [0] * (N + 1)
    for i in range(2, N + 1):
        t1 = A[i] * (2 * (i - 1) % MOD) % MOD * inv[i] % MOD * inv[i + 1] % MOD
        t2 = A[i] * inv[i] % MOD
        P1[i] = (P1[i - 1] + t1) % MOD
        P2[i] = (P2[i - 1] + t2) % MOD

    out = []
    for _ in range(Q):
        u = int(data[pos]); v = int(data[pos + 1]); pos += 2
        res = P1[u - 1]
        if u >= 2:
            res = (res + A[u] * (u - 1) % MOD * inv[u]) % MOD
        res = (res + P2[v - 1] - P2[u]) % MOD
        res = (res + A[v]) % MOD
        out.append(str(fact * res % MOD))
    sys.stdout.write("\n".join(out) + "\n")

solve()