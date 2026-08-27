import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    N = next(it)
    Q = next(it)

    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = next(it) % MOD

    inv = [0] * (N + 1)
    inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    pref = [0] * (N + 1)
    for i in range(2, N + 1):
        pref[i] = (pref[i - 1] + A[i] * inv[i]) % MOD

    # C[i] = expected sum of distances from i to all vertices 1..i-1.
    # B[i] = C[i] / i.
    B = [0] * (N + 1)
    pair_sum = 0  # Expected sum of distances over all unordered pairs so far.

    for i in range(2, N + 1):
        c = ((i - 1) * A[i] + 2 * pair_sum * inv[i - 1]) % MOD
        B[i] = c * inv[i] % MOD
        pair_sum = (pair_sum + c) % MOD

    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD

    out = []
    for _ in range(Q):
        u = next(it)
        v = next(it)

        # u < v:
        # E[d(u,v)] = A[v] + B[u] + sum_{k=u+1}^{v-1} A[k]/k
        expected = (A[v] + B[u] + pref[v - 1] - pref[u]) % MOD
        out.append(str(expected * fact % MOD))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()