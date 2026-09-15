import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)
    N = next(it)
    Q = next(it)

    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = next(it) % MOD

    # modular inverses up to N+1
    inv = [0] * (N + 2)
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    prefixC = [0] * (N + 2)
    prefixInv = [0] * (N + 2)

    for i in range(2, N + 1):
        # term for i < u < v : 2 * (i - 1) / (i * (i + 1))
        termC = A[i] * (2 * (i - 1) % MOD) % MOD
        termC = termC * inv[i] % MOD
        termC = termC * inv[i + 1] % MOD
        prefixC[i] = (prefixC[i - 1] + termC) % MOD

        # term for u < i < v : 1 / i
        termI = A[i] * inv[i] % MOD
        prefixInv[i] = (prefixInv[i - 1] + termI) % MOD

    fact = 1
    for x in range(2, N):
        fact = fact * x % MOD

    out = []
    for _ in range(Q):
        u = next(it)
        v = next(it)

        if u == 1:
            S = (prefixInv[v - 1] + A[v]) % MOD
        else:
            S = prefixC[u - 1]
            S = (S + A[u] * (u - 1) % MOD * inv[u]) % MOD
            S = (S + prefixInv[v - 1] - prefixInv[u]) % MOD
            S = (S + A[v]) % MOD

        ans = S * fact % MOD
        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()