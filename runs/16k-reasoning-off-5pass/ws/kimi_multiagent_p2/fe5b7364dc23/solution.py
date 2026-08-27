import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    K = int(data[1])
    A = data[2:2 + n]

    # Binomial coefficients C(K, t) via Pascal's rule
    C = [[0] * (K + 1) for _ in range(K + 1)]
    for i in range(K + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD
    comb = C[K]

    # G[t] = sum over seen prefix sums S_j of (-1)^t * S_j^t  (mod MOD)
    G = [0] * (K + 1)
    G[0] = 1  # S_0 = 0 contributes 1 to t=0, 0 to t>0

    ans = 0
    S = 0
    for idx in range(n):
        S = (S + int(A[idx])) % MOD

        # powers of S: pw[e] = S^e
        pw = [1] * (K + 1)
        for e in range(1, K + 1):
            pw[e] = pw[e - 1] * S % MOD

        # contribution of subarrays ending at current position:
        # sum_{j<i} (S_i - S_j)^K = sum_t C(K,t) S_i^{K-t} * G[t]
        contrib = 0
        for t in range(K + 1):
            contrib = (contrib + comb[t] * pw[K - t] % MOD * G[t]) % MOD
        ans = (ans + contrib) % MOD

        # add current prefix sum S into aggregates: (-1)^t * S^t
        for t in range(K + 1):
            if t & 1:
                G[t] = (G[t] - pw[t]) % MOD
            else:
                G[t] = (G[t] + pw[t]) % MOD

    print(ans % MOD)

main()