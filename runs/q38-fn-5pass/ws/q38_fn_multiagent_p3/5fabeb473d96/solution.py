import sys

MOD = 998244353

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, Q = data[0], data[1]
    A = [0] * (N + 1)

    idx = 2
    for i in range(2, N + 1):
        A[i] = data[idx] % MOD
        idx += 1

    # Modular inverses up to N+1.
    inv = [0] * (N + 2)
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # pref_b[k] = sum_{i=2..k} A_i * 2(i-1) / (i(i+1))
    # pref_c[k] = sum_{i=2..k} A_i / i
    pref_b = [0] * (N + 1)
    pref_c = [0] * (N + 1)

    for i in range(2, N + 1):
        ai = A[i]
        pref_c[i] = (pref_c[i - 1] + ai * inv[i]) % MOD
        pref_b[i] = (
            pref_b[i - 1]
            + ai * 2 * (i - 1) % MOD * inv[i] % MOD * inv[i + 1]
        ) % MOD

    # (N-1)! modulo MOD
    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD

    out = []
    for _ in range(Q):
        u = data[idx]
        v = data[idx + 1]
        idx += 2

        # Expected distance modulo MOD, before multiplying by (N-1)!.
        res = pref_b[u - 1]

        # Edge u: present on path iff u is not an ancestor of v.
        if u >= 2:
            res += A[u] * (1 - inv[u]) % MOD

        # Edges strictly between u and v: present iff ancestor of v.
        if v > u + 1:
            res += pref_c[v - 1] - pref_c[u]

        # Edge v is always on the path from u to v.
        res += A[v]

        out.append(str((res % MOD) * fact % MOD))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()