import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, q = data[0], data[1]
    pos = 2

    a = [0] * (n + 1)
    for i in range(2, n + 1):
        a[i] = data[pos] % MOD
        pos += 1

    inv = [0] * (n + 2)
    inv[1] = 1
    for i in range(2, n + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # ordinary[i] = sum_{k=2..i} A_k / k
    ordinary = [0] * (n + 1)

    # early[i] = sum_{k=2..i} A_k * 2(k-1)/(k(k+1))
    early = [0] * (n + 1)

    for k in range(2, n + 1):
        ordinary[k] = (ordinary[k - 1] + a[k] * inv[k]) % MOD
        coeff = 2 * (k - 1) % MOD * inv[k] % MOD * inv[k + 1] % MOD
        early[k] = (early[k - 1] + a[k] * coeff) % MOD

    fact = 1
    for x in range(1, n):
        fact = fact * x % MOD

    out = []
    for _ in range(q):
        u = data[pos]
        v = data[pos + 1]
        pos += 2

        # Edges k<u.
        expected = early[u - 1]

        # Edge u.
        if u >= 2:
            expected += a[u] * (u - 1) % MOD * inv[u]

        # Edges u<k<v.
        expected += ordinary[v - 1] - ordinary[u]

        # Edge v.
        expected += a[v]

        out.append(str((expected % MOD) * fact % MOD))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()