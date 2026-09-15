import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, Q = data[0], data[1]
    A = [0] * (N + 1)

    idx = 2
    for i in range(2, N + 1):
        A[i] = data[idx] % MOD
        idx += 1

    # Modular inverses up to N + 1.
    inv = [0] * (N + 2)
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # pref_inv[x] = sum_{i=2}^x A_i / i
    # pref_c[x]   = sum_{i=2}^x A_i * 2(i-1)/(i(i+1))
    pref_inv = [0] * (N + 1)
    pref_c = [0] * (N + 1)

    for i in range(2, N + 1):
        pref_inv[i] = (pref_inv[i - 1] + A[i] * inv[i]) % MOD
        c = (2 * (i - 1) % MOD) * inv[i] % MOD * inv[i + 1] % MOD
        pref_c[i] = (pref_c[i - 1] + A[i] * c) % MOD

    # (N-1)! modulo MOD
    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD

    out = []
    for _ in range(Q):
        u = data[idx]
        v = data[idx + 1]
        idx += 2

        # Expected distance as a modular rational number.
        exp = A[v]  # edge i = v always separates u and v

        # edge i = u: separates iff v is not in subtree of u
        if u >= 2:
            exp = (exp + A[u] * (1 - inv[u])) % MOD

        # edges u < i < v: probability 1/i
        if u + 1 <= v - 1:
            exp = (exp + pref_inv[v - 1] - pref_inv[u]) % MOD

        # edges 2 <= i < u: probability 2(i-1)/(i(i+1))
        exp = (exp + pref_c[u - 1]) % MOD

        out.append(str(exp * fact % MOD))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()