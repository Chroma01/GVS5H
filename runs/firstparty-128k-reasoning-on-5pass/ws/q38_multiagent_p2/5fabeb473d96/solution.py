import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    it = iter(data)
    N = next(it)
    Q = next(it)

    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = next(it) % MOD

    inv = [0] * (N + 2)
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD

    prefB = [0] * (N + 1)
    prefC = [0] * (N + 1)

    for i in range(2, N + 1):
        ai = A[i]

        termB = ai * (2 * i - 2) % MOD
        termB = termB * inv[i] % MOD
        termB = termB * inv[i + 1] % MOD
        prefB[i] = (prefB[i - 1] + termB) % MOD

        prefC[i] = (prefC[i - 1] + ai * inv[i]) % MOD

    out = []
    for _ in range(Q):
        u = next(it)
        v = next(it)

        termU = A[u] * (u - 1) % MOD
        termU = termU * inv[u] % MOD

        ans = (
            prefB[u - 1]
            + termU
            + prefC[v - 1]
            - prefC[u]
            + A[v]
        ) % MOD

        ans = ans * fact % MOD
        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()