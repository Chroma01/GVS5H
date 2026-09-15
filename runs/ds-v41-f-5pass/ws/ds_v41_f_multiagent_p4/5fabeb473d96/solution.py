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

    # modular inverses up to N+1
    size = N + 2
    inv = [0] * size
    inv[1] = 1
    for i in range(2, size):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    # pre1[k] = sum_{i=2..k} A_i * 2(i-1)/(i(i+1))   (coefficient for i < u)
    # pre2[k] = sum_{i=2..k} A_i / i                  (coefficient for u < i < v)
    pre1 = [0] * (N + 1)
    pre2 = [0] * (N + 1)
    for k in range(2, N + 1):
        ak = A[k] % MOD
        pre1[k] = (pre1[k - 1] + ak * (2 * (k - 1) % MOD) % MOD * inv[k] % MOD * inv[k + 1]) % MOD
        pre2[k] = (pre2[k - 1] + ak * inv[k]) % MOD

    # fact = (N-1)!
    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD

    out = []
    for _ in range(Q):
        u = int(data[pos]); pos += 1
        v = int(data[pos]); pos += 1
        # coefficient summary:
        #   i < u        : 2(i-1)/(i(i+1))
        #   i = u (u>1)  : (u-1)/u
        #   u < i < v    : 1/i
        #   i = v        : 1
        S = pre1[u - 1]
        if u >= 2:
            S = (S + A[u] % MOD * (u - 1) % MOD * inv[u]) % MOD
        S = (S + pre2[v - 1] - pre2[u]) % MOD
        S = (S + A[v]) % MOD
        out.append(str(S * fact % MOD))

    sys.stdout.write("\n".join(out) + "\n")

main()