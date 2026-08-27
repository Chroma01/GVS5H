import sys

MOD = 998244353


def solve():
    input = sys.stdin.buffer.readline

    n, q = map(int, input().split())
    a = [0] * (n + 2)

    values = list(map(int, input().split()))
    for i, value in enumerate(values, 2):
        a[i] = value % MOD

    inv = [0] * (n + 3)
    inv[1] = 1
    for i in range(2, n + 3):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # Prefix sums:
    # pref_mid[x] = sum_{2 <= k <= x} A_k / k
    # pref_sep[x] = sum_{2 <= k <= x} A_k * 2(k-1)/(k(k+1))
    pref_mid = [0] * (n + 1)
    pref_sep = [0] * (n + 1)

    for k in range(2, n + 1):
        pref_mid[k] = (pref_mid[k - 1] + a[k] * inv[k]) % MOD

        probability = (
            2 * (k - 1) % MOD * inv[k] % MOD * inv[k + 1]
        ) % MOD
        pref_sep[k] = (
            pref_sep[k - 1] + a[k] * probability
        ) % MOD

    total_trees = 1
    for i in range(1, n):
        total_trees = total_trees * i % MOD

    answers = []

    for _ in range(q):
        u, v = map(int, input().split())

        expected = 0

        # Edge u: it separates u and v unless u is an ancestor of v.
        if u >= 2:
            expected += a[u] * (1 - inv[u])

        # Edges k with u < k < v: k can only be an ancestor of v,
        # which happens with probability 1/k.
        expected += pref_mid[v - 1] - pref_mid[u]

        # Edge v always belongs to the path.
        expected += a[v]

        # Edges k < u: the corrected separation probability is
        # 2(k-1)/(k(k+1)), independent of u and v.
        if u >= 2:
            expected += pref_sep[u - 1]

        expected %= MOD
        answers.append(str(expected * total_trees % MOD))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()