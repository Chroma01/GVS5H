import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    q = next(it)

    a = [0] * (n + 1)
    for i in range(2, n + 1):
        a[i] = next(it) % MOD

    inv = [0] * (n + 1)
    inv[1] = 1
    for i in range(2, n + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # pref_xor[k] = sum_{i=2..k} A_i * 2(i-1)/(i(i+1))
    # pref_inv[k] = sum_{i=2..k} A_i / i
    pref_xor = [0] * (n + 1)
    pref_inv = [0] * (n + 1)

    for i in range(2, n + 1):
        coeff = 2 * (i - 1) % MOD
        coeff = coeff * inv[i] % MOD * inv[i + 1] % MOD if i < n else coeff * inv[i] % MOD * pow(i + 1, MOD - 2, MOD) % MOD
        # The conditional expression above avoids requiring inv[n+1] in the array.
        pref_xor[i] = (pref_xor[i - 1] + a[i] * coeff) % MOD
        pref_inv[i] = (pref_inv[i - 1] + a[i] * inv[i]) % MOD

    fact = 1
    for x in range(2, n):
        fact = fact * x % MOD

    out = []
    for _ in range(q):
        u = next(it)
        v = next(it)

        # Input guarantees u < v.
        expected = pref_xor[u - 1]

        if u >= 2:
            expected += a[u] * (1 - inv[u])
        expected += pref_inv[v - 1] - pref_inv[u]
        expected += a[v]

        expected %= MOD
        out.append(str(expected * fact % MOD))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()