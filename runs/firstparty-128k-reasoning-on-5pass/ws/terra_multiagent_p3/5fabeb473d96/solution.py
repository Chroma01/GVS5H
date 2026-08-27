import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    N = next(it)
    Q = next(it)

    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = next(it) % MOD

    inv = [0] * (N + 1)
    inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    pref_low = [0] * (N + 1)
    pref_mid = [0] * (N + 1)

    for i in range(2, N + 1):
        low_coef = 2 * (i - 1) % MOD * inv[i] % MOD * inv[i + 1] % MOD if i < N else 0
        # pref_low is only queried through u-1, so coefficient for N is unnecessary.
        pref_low[i] = (pref_low[i - 1] + A[i] * low_coef) % MOD
        pref_mid[i] = (pref_mid[i - 1] + A[i] * inv[i]) % MOD

    fact = 1
    for x in range(1, N):
        fact = fact * x % MOD

    out = []
    for _ in range(Q):
        u = next(it)
        v = next(it)

        expected = pref_low[u - 1]

        if u >= 2:
            expected += A[u] * (u - 1) % MOD * inv[u] % MOD

        expected += pref_mid[v - 1] - pref_mid[u]
        expected += A[v]
        expected %= MOD

        out.append(str(expected * fact % MOD))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()