import sys

MOD = 998244353


def _verify_small(n):
    """
    Brute-force verifier for the edge-separation coefficients.
    Runs only for very small n.
    """
    from itertools import product

    choices = [range(1, i) for i in range(2, n + 1)]
    counts = {
        (u, v, x): 0
        for u in range(1, n + 1)
        for v in range(u + 1, n + 1)
        for x in range(2, n + 1)
    }

    total = 0
    for ps in product(*choices):
        total += 1
        par = [0] * (n + 1)
        for i, p in enumerate(ps, 2):
            par[i] = p

        def anc(x, y):
            while y >= x:
                if y == x:
                    return True
                y = par[y]
            return False

        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                for x in range(2, n + 1):
                    if anc(x, u) ^ anc(x, v):
                        counts[(u, v, x)] += 1

    for (u, v, x), cnt in counts.items():
        if x < u:
            num, den = 2 * (x - 1), x * (x + 1)
        elif x == u:
            num, den = u - 1, u
        elif x < v:
            num, den = 1, x
        elif x == v:
            num, den = 1, 1
        else:
            num, den = 0, 1

        if cnt * den != total * num:
            raise AssertionError("coefficient mismatch")


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, Q = data[0], data[1]

    # Optional brute-force verification for tiny cases.
    if N <= 5:
        _verify_small(N)

    A = [0] * (N + 1)
    pos = 2
    for i in range(2, N + 1):
        A[i] = data[pos] % MOD
        pos += 1

    # Modular inverses up to N+1.
    inv = [0] * (N + 2)
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # (N-1)! modulo MOD.
    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD

    # pref1[t] = sum_{x=2}^t A_x / x
    # pref2[t] = sum_{x=2}^t A_x * 2(x-1) / (x(x+1))
    pref1 = [0] * (N + 1)
    pref2 = [0] * (N + 1)

    for x in range(2, N + 1):
        ax = A[x]
        pref1[x] = (pref1[x - 1] + ax * inv[x]) % MOD
        coef2 = (2 * (x - 1) % MOD) * inv[x] % MOD * inv[x + 1] % MOD
        pref2[x] = (pref2[x - 1] + ax * coef2) % MOD

    out = []
    for _ in range(Q):
        u = data[pos]
        v = data[pos + 1]
        pos += 2

        # Expected distance modulo MOD:
        # pref2[u-1]
        # + A_u * (u-1)/u
        # + pref1[v-1] - pref1[u]
        # + A_v
        ans = pref2[u - 1]
        ans = (ans + A[u] * (u - 1) % MOD * inv[u]) % MOD
        ans = (ans + pref1[v - 1] - pref1[u]) % MOD
        ans = (ans + A[v]) % MOD

        out.append(str(ans * fact % MOD))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()