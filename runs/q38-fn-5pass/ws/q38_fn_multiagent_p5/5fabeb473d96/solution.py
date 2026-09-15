import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, Q = data[0], data[1]
    A = [0] * (N + 2)

    pos = 2
    for i in range(2, N + 1):
        A[i] = data[pos] % MOD
        pos += 1

    # Modular inverses up to N+1.
    inv = [0] * (N + 2)
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # pref_inv[i] = sum_{k=2}^i A_k / k
    # pref_c[i]   = sum_{k=2}^i A_k * 2(k-1) / (k(k+1))
    pref_inv = [0] * (N + 2)
    pref_c = [0] * (N + 2)

    for i in range(2, N + 1):
        ai = A[i]

        pref_inv[i] = (pref_inv[i - 1] + ai * inv[i]) % MOD

        c = ai * (2 * (i - 1) % MOD) % MOD
        c = c * inv[i] % MOD
        c = c * inv[i + 1] % MOD
        pref_c[i] = (pref_c[i - 1] + c) % MOD

    # (N-1)! modulo MOD
    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD

    out = []
    mod = MOD

    for _ in range(Q):
        u = data[pos]
        v = data[pos + 1]
        pos += 2

        # Expected distance in a uniformly random recursive tree.
        exp = A[v]

        # Edges k with u < k < v: probability 1/k.
        exp += pref_inv[v - 1] - pref_inv[u]

        if u >= 2:
            # Edge k = u: probability 1 - 1/u = (u-1)/u.
            exp += A[u] * (u - 1) % mod * inv[u] % mod

            # Edges k with 2 <= k < u: probability 2(k-1)/(k(k+1)).
            exp += pref_c[u - 1]

        exp %= mod
        out.append(str(exp * fact % mod))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()