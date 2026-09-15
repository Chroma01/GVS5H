import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    Q = int(data[idx]); idx += 1
    MOD = 998244353

    # A[i] for i = 2..N ; A[1] stays 0
    A = [0] * (N + 2)
    for i in range(2, N + 1):
        A[i] = int(data[idx]); idx += 1

    # modular inverses of 1..N+1
    inv = [0] * (N + 2)
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i]) % MOD

    # S1[i] = sum_{k=2}^{i} A_k / k
    # S2[i] = sum_{k=2}^{i} A_k * 2(k-1)/(k(k+1))
    S1 = [0] * (N + 2)
    S2 = [0] * (N + 2)
    for i in range(2, N + 1):
        S1[i] = (S1[i - 1] + A[i] * inv[i]) % MOD
        S2[i] = (S2[i - 1] + A[i] * (2 * (i - 1)) % MOD * inv[i] % MOD * inv[i + 1]) % MOD

    # (N-1)!
    fact = 1
    for k in range(2, N):
        fact = fact * k % MOD

    out = []
    for _ in range(Q):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        inner = S2[u - 1]                                    # edges i < u
        inner = (inner + A[u] * (u - 1) % MOD * inv[u]) % MOD  # edge i = u
        inner = (inner + S1[v - 1] - S1[u]) % MOD            # edges u < i < v
        inner = (inner + A[v]) % MOD                          # edge i = v
        out.append(str(inner * fact % MOD))

    sys.stdout.write("\n".join(out) + "\n")

main()