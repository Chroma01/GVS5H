import sys

MOD = 998244353

def solve():
    input = sys.stdin.buffer.readline

    n, q = map(int, input().split())
    a = [0] * (n + 1)
    vals = list(map(int, input().split()))
    for i, x in enumerate(vals, start=2):
        a[i] = x % MOD

    prefix_before = [0] * (n + 1)
    prefix_between = [0] * (n + 1)

    for i in range(2, n + 1):
        inv_i = pow(i, MOD - 2, MOD)

        # Coefficient for an edge i with i < u:
        # 2(i-1)/(i(i+1))
        coeff_before = 2 * (i - 1) * inv_i % MOD * pow(i + 1, MOD - 2, MOD) % MOD

        # Coefficient for an edge i with u < i < v:
        # 1/i
        coeff_between = inv_i

        prefix_before[i] = (prefix_before[i - 1] + a[i] * coeff_before) % MOD
        prefix_between[i] = (prefix_between[i - 1] + a[i] * coeff_between) % MOD

    total_trees = 1
    for i in range(2, n + 1):
        total_trees = total_trees * (i - 1) % MOD

    out = []
    for _ in range(q):
        u, v = map(int, input().split())

        # Edges with index i < u.
        expected = prefix_before[u - 1]

        # Edge u itself, unless u is the root.
        if u >= 2:
            expected += a[u] * (u - 1) % MOD * pow(u, MOD - 2, MOD) % MOD
            expected %= MOD

        # Edges u < i < v.
        expected += prefix_between[v - 1] - prefix_between[u]
        expected %= MOD

        # Edge v always belongs to the path because v is an endpoint.
        expected += a[v]
        expected %= MOD

        out.append(str(expected * total_trees % MOD))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()