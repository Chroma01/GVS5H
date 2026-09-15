import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]
    A = data[2:2 + N]

    # Binomial coefficients up to K.
    C = [[0] * (K + 1) for _ in range(K + 1)]
    for n in range(K + 1):
        C[n][0] = C[n][n] = 1
        for r in range(1, n):
            C[n][r] = (C[n - 1][r - 1] + C[n - 1][r]) % MOD

    # M[s] = sum_{i < current j} P[i]^s
    # Initially only P[0] = 0 is present.
    M = [0] * (K + 1)
    M[0] = 1

    ans = 0
    pref = 0

    for a in A:
        pref = (pref + a) % MOD

        pw = [1] * (K + 1)
        for t in range(1, K + 1):
            pw[t] = pw[t - 1] * pref % MOD

        # Add sum_{i<j} (P[j] - P[i])^K
        # = sum_t C(K,t) * P[j]^t * (-1)^(K-t) * sum_i P[i]^(K-t)
        for t in range(K + 1):
            s = K - t
            term = C[K][t] * pw[t] % MOD * M[s] % MOD
            if s & 1:
                ans -= term
            else:
                ans += term
        ans %= MOD

        # P[j] becomes an earlier prefix sum for future j.
        for s in range(K + 1):
            M[s] = (M[s] + pw[s]) % MOD

    print(ans % MOD)

if __name__ == "__main__":
    main()