import sys

MOD = 998244353

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    N = next(it)
    Q = next(it)

    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = next(it) % MOD

    inv = [0] * (N + 2)
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    pref_xor = [0] * (N + 1)
    pref_anc = [0] * (N + 1)

    for i in range(2, N + 1):
        # For i < u, probability that edge i separates u and v:
        # 2 * (i - 1) / (i * (i + 1)).
        coeff = 2 * (i - 1) % MOD * inv[i] % MOD * inv[i + 1] % MOD
        pref_xor[i] = (
            pref_xor[i - 1] + A[i] * coeff
        ) % MOD

        # For u < i < v, probability that edge i lies on the path:
        # 1 / i.
        pref_anc[i] = (
            pref_anc[i - 1] + A[i] * inv[i]
        ) % MOD

    factorial = 1
    for i in range(2, N):
        factorial = factorial * i % MOD

    out = []
    for _ in range(Q):
        u = next(it)
        v = next(it)

        ans = pref_xor[u - 1]

        # Edge u, when u >= 2: it is on the path unless u is an ancestor of v.
        if u >= 2:
            ans += A[u] * (u - 1) % MOD * inv[u] % MOD

        # Edges strictly between u and v.
        ans += pref_anc[v - 1] - pref_anc[u]
        ans += A[v]  # Edge v always lies on the path.

        ans %= MOD
        out.append(str(ans * factorial % MOD))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()