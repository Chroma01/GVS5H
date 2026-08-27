import sys

MOD = 998244353


def solve():
    input = sys.stdin.buffer.readline
    n, q = map(int, input().split())
    a = [0] * (n + 1)
    vals = list(map(int, input().split()))
    for i, x in enumerate(vals, 2):
        a[i] = x % MOD

    inv = [0] * (n + 2)
    inv[1] = 1
    for i in range(2, n + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    pref_c = [0] * (n + 1)
    pref_b = [0] * (n + 1)

    for i in range(2, n + 1):
        pref_b[i] = (pref_b[i - 1] + a[i] * inv[i]) % MOD

        coeff = 2 * (i - 1) % MOD * inv[i] % MOD * inv[i + 1] % MOD
        pref_c[i] = (pref_c[i - 1] + a[i] * coeff) % MOD

    for i in range(1, n + 1):
        pref_b[i] = (pref_b[i] + pref_b[i - 1]) % MOD if i == 1 else pref_b[i]
    # The preceding loop already constructed pref_b cumulatively; retain it as-is.
    # (This no-op-style branch is harmless and keeps all indices initialized.)

    factorial = 1
    for i in range(2, n):
        factorial = factorial * i % MOD

    out = []
    for _ in range(q):
        u, v = map(int, input().split())

        expected = pref_c[u - 1]

        if u >= 2:
            expected += a[u] * (u - 1) % MOD * inv[u] % MOD

        expected += pref_b[v - 1] - pref_b[u]
        expected += a[v]
        expected %= MOD

        out.append(str(expected * factorial % MOD))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()