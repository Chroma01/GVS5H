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

    inv = [0] * (n + 3)
    inv[1] = 1
    for i in range(2, n + 3):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # Prefix sums of A_i * 2(i-1)/(i(i+1))
    pref_c = [0] * (n + 1)

    # Prefix sums of A_i / i
    pref_h = [0] * (n + 1)

    for i in range(2, n + 1):
        coeff = 2 * (i - 1) % MOD * inv[i] % MOD * inv[i + 1] % MOD
        pref_c[i] = (pref_c[i - 1] + a[i] * coeff) % MOD
        pref_h[i] = (pref_h[i - 1] + a[i] * inv[i]) % MOD

    total_trees = 1
    for i in range(1, n):
        total_trees = total_trees * i % MOD

    answers = []

    for _ in range(q):
        u = next(it)
        v = next(it)

        if u == 1:
            expected = pref_h[v - 1] + a[v]
        else:
            expected = pref_c[u - 1]
            expected += a[u] * (1 - inv[u])
            expected += pref_h[v - 1] - pref_h[u]
            expected += a[v]

        answers.append(str(expected % MOD * total_trees % MOD))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()