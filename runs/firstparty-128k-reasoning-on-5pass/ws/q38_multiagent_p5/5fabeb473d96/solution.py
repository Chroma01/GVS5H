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

    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD

    pref1 = [0] * (N + 1)
    pref2 = [0] * (N + 1)
    spec = [0] * (N + 1)

    for i in range(2, N + 1):
        ai = A[i]
        inv_i = inv[i]

        t2 = ai * inv_i % MOD
        pref2[i] = (pref2[i - 1] + t2) % MOD

        spec[i] = ai - t2
        if spec[i] < 0:
            spec[i] += MOD

        t1 = t2 * 2 % MOD
        t1 = t1 * (i - 1) % MOD
        t1 = t1 * inv[i + 1] % MOD
        pref1[i] = (pref1[i - 1] + t1) % MOD

    out = []
    p1 = pref1
    p2 = pref2
    sp = spec
    Al = A
    f = fact
    mod = MOD

    for _ in range(Q):
        u = data[idx]
        v = data[idx + 1]
        idx += 2

        val = (p1[u - 1] + sp[u] + p2[v - 1] - p2[u] + Al[v]) % mod
        out.append(str(val * f % mod))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()