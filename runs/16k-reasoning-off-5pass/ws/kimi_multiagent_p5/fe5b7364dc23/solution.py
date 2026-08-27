import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    A = list(map(int, data[2:2 + n]))

    # Binomial coefficients C(k, b) mod MOD via Pascal's rule
    C = [[0] * (k + 1) for _ in range(k + 1)]
    for i in range(k + 1):
        C[i][0] = C[i][i] = 1
        for j in range(1, i):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD

    # T[a] = sum over already-seen prefix sums S_j of S_j^a
    # Initialize with S_0 = 0: 0^0 = 1, 0^a = 0 for a >= 1
    T = [0] * (k + 1)
    T[0] = 1

    ans = 0
    S = 0  # current prefix sum mod MOD
    for i in range(n):
        S = (S + A[i]) % MOD
        # powers of S: pw[b] = S^b
        pw = [1] * (k + 1)
        for b in range(1, k + 1):
            pw[b] = pw[b - 1] * S % MOD
        # add contributions of pairs (j, r=i+1) with j < r
        # (S_r - S_j)^K = sum_b C(K,b) * S_r^b * (-1)^(K-b) * S_j^(K-b)
        for b in range(k + 1):
            term = C[k][b] * pw[b] % MOD * T[k - b] % MOD
            if (k - b) & 1:
                ans -= term
            else:
                ans += term
        ans %= MOD
        # update running totals with current prefix sum
        for a in range(k + 1):
            T[a] = (T[a] + pw[a]) % MOD

    print(ans % MOD)

main()