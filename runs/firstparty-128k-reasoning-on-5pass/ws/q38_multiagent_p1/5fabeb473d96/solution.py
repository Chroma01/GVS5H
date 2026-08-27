import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    Q = data[1]

    A = [0] * (N + 1)
    idx = 2
    for i in range(2, N + 1):
        A[i] = data[idx] % MOD
        idx += 1

    inv = [0] * (N + 2)
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    S1 = [0] * (N + 1)
    S2 = [0] * (N + 1)

    for i in range(2, N + 1):
        ai = A[i]
        c1 = (2 * (i - 1) % MOD) * inv[i] % MOD * inv[i + 1] % MOD
        S1[i] = (S1[i - 1] + ai * c1) % MOD
        S2[i] = (S2[i - 1] + ai * inv[i]) % MOD

    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD

    out = []
    s1 = S1
    s2 = S2
    a = A
    invl = inv
    mod = MOD
    f = fact

    for _ in range(Q):
        u = data[idx]
        v = data[idx + 1]
        idx += 2

        res = (
            s1[u - 1]
            + a[u] * (1 - invl[u])
            + s2[v - 1]
            - s2[u]
            + a[v]
        ) % mod
        out.append(str(res * f % mod))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()