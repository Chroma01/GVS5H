import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    Q = data[1]

    # After this, data[i] is A_i modulo MOD for 2 <= i <= N.
    for i in range(2, N + 1):
        data[i] %= MOD

    # Modular inverses up to N+1.
    inv = [0] * (N + 2)
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # prefB[i] = sum_{2 <= k <= i} A_k / k
    # prefC[i] = sum_{2 <= k <= i} A_k * 2(k-1) / (k(k+1))
    # extra[i] = A_i * (1 - 1/i), extra[1] = 0
    prefB = [0] * (N + 1)
    prefC = [0] * (N + 1)
    extra = [0] * (N + 1)

    for i in range(2, N + 1):
        ai = data[i]
        extra[i] = ai * (1 - inv[i]) % MOD
        prefB[i] = (prefB[i - 1] + ai * inv[i]) % MOD

        c = (2 * (i - 1)) % MOD
        c = c * inv[i] % MOD
        c = c * inv[i + 1] % MOD
        prefC[i] = (prefC[i - 1] + ai * c) % MOD

    # (N-1)! modulo MOD
    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD

    out = []
    append = out.append

    idx = N + 1
    a = data
    pb = prefB
    pc = prefC
    ex = extra
    f = fact
    mod = MOD

    for _ in range(Q):
        u = a[idx]
        v = a[idx + 1]
        idx += 2

        term = a[v] + ex[u] + pb[v - 1] - pb[u] + pc[u - 1]
        append(str((term % mod) * f % mod))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()