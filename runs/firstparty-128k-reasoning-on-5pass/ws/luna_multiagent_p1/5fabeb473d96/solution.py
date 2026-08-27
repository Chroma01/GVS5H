import sys

MOD = 998244353


def solve():
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

    # pref_middle[x] = sum_{i=2..x} A_i / i
    pref_middle = [0] * (n + 1)

    # pref_early[x] = sum_{i=2..x} A_i * 2(i-1)/(i(i+1))
    pref_early = [0] * (n + 1)

    for i in range(2, n + 1):
        pref_middle[i] = (
            pref_middle[i - 1] + a[i] * inv[i]
        ) % MOD

        coeff = 2 * (i - 1) % MOD * inv[i] % MOD * inv[i + 1] % MOD
        pref_early[i] = (
            pref_early[i - 1] + a[i] * coeff
        ) % MOD

    total_trees = 1
    for i in range(2, n):
        total_trees = total_trees * i % MOD

    out = []

    for _ in range(q):
        u = next(it)
        v = next(it)

        expected_sum = 0

        # Edges i < u.
        if u >= 2:
            expected_sum += pref_early[u - 1]

            # Edge i = u.
            expected_sum += a[u] * (1 - inv[u]) % MOD

        # Edges u < i < v.
        expected_sum += (pref_middle[v - 1] - pref_middle[u]) % MOD

        # Edge i = v.
        expected_sum += a[v]

        expected_sum %= MOD
        out.append(str(expected_sum * total_trees % MOD))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()