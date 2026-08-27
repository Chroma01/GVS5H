import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    K = int(data[1])
    A = data[2:2 + n]

    # Binomial coefficients C(K, j) mod MOD, K <= 10
    C = [[0] * (K + 1) for _ in range(K + 1)]
    for i in range(K + 1):
        C[i][0] = C[i][i] = 1
        for j in range(1, i):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD
    binom = C[K]

    # acc[m] = sum over processed prefix sums S_t (t < r) of (-S_t)^m mod MOD
    acc = [0] * (K + 1)
    acc[0] = 1  # t = 0, S_0 = 0 contributes (-0)^0 = 1

    ans = 0
    s = 0  # current prefix sum S_r mod MOD
    for idx in range(n):
        s = (s + int(A[idx])) % MOD

        # powers of s: sp[j] = s^j
        sp = [1] * (K + 1)
        for j in range(1, K + 1):
            sp[j] = sp[j - 1] * s % MOD

        # contribution: sum_j C(K,j) * s^j * acc[K-j]
        contrib = 0
        for j in range(K + 1):
            contrib = (contrib + binom[j] * sp[j] % MOD * acc[K - j]) % MOD
        ans = (ans + contrib) % MOD

        # update acc with (-s)^m
        neg = (-s) % MOD
        p = 1
        for m in range(K + 1):
            acc[m] = (acc[m] + p) % MOD
            p = p * neg % MOD

    print(ans)

main()