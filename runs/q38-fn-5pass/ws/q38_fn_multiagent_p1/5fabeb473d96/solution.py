import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, Q = data[0], data[1]
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

    # pref_inv[k] = sum_{i=2..k} A_i / i
    # pref_pre[k] = sum_{i=2..k} A_i * 2(i-1) / (i(i+1))
    # self_coef[i] = A_i * (i-1) / i
    pref_inv = [0] * (N + 1)
    pref_pre = [0] * (N + 1)
    self_coef = [0] * (N + 1)

    for i in range(2, N + 1):
        ai = A[i]
        pref_inv[i] = (pref_inv[i - 1] + ai * inv[i]) % MOD
        pref_pre[i] = (
            pref_pre[i - 1]
            + ai * (2 * (i - 1) % MOD) % MOD * inv[i] % MOD * inv[i + 1] % MOD
        ) % MOD
        self_coef[i] = ai * (i - 1) % MOD * inv[i] % MOD

    # (N-1)! modulo MOD
    fact = 1
    for i in range(1, N):
        fact = fact * i % MOD

    out = []
    p_inv = pref_inv
    p_pre = pref_pre
    sc = self_coef
    inv_l = inv
    A_l = A
    mod = MOD
    f = fact

    for _ in range(Q):
        u = data[pos]
        v = data[pos + 1]
        pos += 2

        # Sum over all edges i of A_i * Pr(edge i is on path u-v).
        res = p_pre[u - 1]

        if u > 1:
            res += sc[u]

        # Edges u < i < v have coefficient 1/i.
        res += p_inv[v - 1] - p_inv[u]

        # Edge v is always on the path.
        res += A_l[v]

        res %= mod
        out.append(str(res * f % mod))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()