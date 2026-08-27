import sys

def main():
    MOD = 998244353
    data = list(map(int, sys.stdin.buffer.read().split()))
    pos = 0
    N = data[pos]; Q = data[pos + 1]; pos += 2

    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = data[pos] % MOD
        pos += 1

    # modular inverses of 1..N+1 via linear recurrence
    inv = [0] * (N + 2)
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # B[x] = sum_{k=2..x} A_k / k
    # C[x] = sum_{k=2..x} A_k * 2(k-1) / (k(k+1))
    B = [0] * (N + 1)
    C = [0] * (N + 1)
    for k in range(2, N + 1):
        B[k] = (B[k - 1] + A[k] * inv[k]) % MOD
        C[k] = (C[k - 1] + A[k] * (2 * (k - 1) % MOD) % MOD * inv[k] % MOD * inv[k + 1]) % MOD

    # (N-1)!
    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD

    out = []
    for _ in range(Q):
        u = data[pos]; v = data[pos + 1]; pos += 2
        s = C[u - 1] + B[v - 1] - B[u] + A[v]
        if u >= 2:
            s += A[u] * (1 - inv[u])
        s %= MOD
        out.append(str(fact * s % MOD))

    sys.stdout.write("\n".join(out) + "\n")

main()