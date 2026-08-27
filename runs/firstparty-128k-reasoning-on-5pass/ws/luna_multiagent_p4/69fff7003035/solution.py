import sys

MOD = 998244353


def solve():
    n = int(sys.stdin.readline())

    counts = {}
    sums = {}
    for x in range(1, n + 1):
        d = len(str(x))
        counts[d] = counts.get(d, 0) + 1
        sums[d] = sums.get(d, 0) + x

    digits = sorted(counts)
    weights = [pow(10, d, MOD) for d in digits]
    cnt = [counts[d] for d in digits]
    value_sum = [sums[d] % MOD for d in digits]
    m = len(digits)

    # Q(t) = product_i (1 + weights[i] * t)
    q = [1]
    for w in weights:
        nq = [0] * (len(q) + 1)
        for j, v in enumerate(q):
            nq[j] = (nq[j] + v) % MOD
            nq[j + 1] = (nq[j + 1] + v * w) % MOD
        q = nq

    # R(t) = sum_i cnt[i] * weights[i] *
    #              product_{j != i} (1 + weights[j] * t)
    r = [0] * m
    for i in range(m):
        other = [1]
        for j in range(m):
            if i == j:
                continue
            w = weights[j]
            no = [0] * (len(other) + 1)
            for k, v in enumerate(other):
                no[k] = (no[k] + v) % MOD
                no[k + 1] = (no[k + 1] + v * w) % MOD
            other = no

        factor = cnt[i] * weights[i] % MOD
        for k, v in enumerate(other):
            r[k] = (r[k] + factor * v) % MOD

    # E[k] = coefficient of t^k in product_i (1 + weights[i] t)^cnt[i].
    # It satisfies Q(t) E'(t) = R(t) E(t).
    e = [0] * (n + 1)
    e[0] = 1
    for k in range(1, n + 1):
        val = 0

        upper_r = min(m - 1, k - 1)
        for j in range(upper_r + 1):
            val += r[j] * e[k - 1 - j]

        upper_q = min(m, k)
        for j in range(1, upper_q + 1):
            val -= q[j] * (k - j) * e[k - j]

        e[k] = (val % MOD) * pow(k, MOD - 2, MOD) % MOD

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    ans = 0
    for i, w in enumerate(weights):
        # g[k] is the coefficient after omitting one element of this class:
        # E(t) = (1 + w t) G(t).
        g_prev = 1
        class_contribution = 0

        for k in range(n):
            g = e[k] if k == 0 else (e[k] - w * g_prev) % MOD
            if k > 0:
                g_prev = g

            ways = fact[k] * fact[n - k - 1] % MOD
            class_contribution = (
                class_contribution + g * ways
            ) % MOD

        ans = (ans + value_sum[i] * class_contribution) % MOD

    print(ans)


if __name__ == "__main__":
    solve()