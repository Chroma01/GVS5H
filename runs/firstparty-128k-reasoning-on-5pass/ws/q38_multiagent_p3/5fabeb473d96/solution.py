import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    idx = 0
    N = data[idx]
    idx += 1
    Q = data[idx]
    idx += 1

    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = data[idx] % MOD
        idx += 1

    inv = [0] * (N + 2)
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD

    pref1 = [0] * (N + 1)
    pref2 = [0] * (N + 1)

    for i in range(2, N + 1):
        ai = A[i]
        pref1[i] = (pref1[i - 1] + ai * inv[i]) % MOD
        pref2[i] = (
            pref2[i - 1]
            + ai * 2 % MOD * (i - 1) % MOD * inv[i] % MOD * inv[i + 1]
        ) % MOD

    out = []
    for _ in range(Q):
        u = data[idx]
        v = data[idx + 1]
        idx += 2

        if u == 1:
            exp = (pref1[v - 1] + A[v]) % MOD
        else:
            exp = (
                pref2[u - 1]
                + A[u] * (u - 1) % MOD * inv[u]
                + (pref1[v - 1] - pref1[u])
                + A[v]
            ) % MOD

        out.append(str(exp * fact % MOD))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()