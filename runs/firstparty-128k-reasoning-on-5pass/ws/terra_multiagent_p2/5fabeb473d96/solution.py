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

    inv = [0] * (n + 2)
    inv[1] = 1
    for i in range(2, n + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # pref_both[k] = sum_{j=2..k} A_j * 2(j-1)/(j(j+1))
    # pref_mid[k]  = sum_{j=2..k} A_j / j
    pref_both = [0] * (n + 1)
    pref_mid = [0] * (n + 1)

    for k in range(2, n + 1):
        coeff_both = 2 * (k - 1) % MOD * inv[k] % MOD * inv[k + 1] % MOD
        pref_both[k] = (pref_both[k - 1] + a[k] * coeff_both) % MOD
        pref_mid[k] = (pref_mid[k - 1] + a[k] * inv[k]) % MOD

    fact = 1
    for x in range(2, n):
        fact = fact * x % MOD

    out = []
    for _ in range(q):
        u = next(it)
        v = next(it)

        expected = a[v]

        if u >= 2:
            expected += pref_both[u - 1]
            expected += a[u] * (u - 1) % MOD * inv[u] % MOD

        if u + 1 <= v - 1:
            expected += pref_mid[v - 1] - pref_mid[u]

        out.append(str(expected % MOD * fact % MOD))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()