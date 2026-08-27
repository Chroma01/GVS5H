import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    a = data[2:2 + n]

    # Binomial coefficients C(K, j) mod MOD via Pascal's rule
    C = [[0] * (k + 1) for _ in range(k + 1)]
    for i in range(k + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD
    comb = C[k]

    # P[j] = sum of S_t^j over all prefix sums S_t seen so far (t < current r)
    # Initialize with S_0 = 0: P[0] = 1, P[j>0] = 0
    P = [0] * (k + 1)
    P[0] = 1

    S = 0
    ans = 0
    for i in range(n):
        S = (S + int(a[i])) % MOD
        # powers pw[e] = S^e mod MOD
        pw = [1] * (k + 1)
        for e in range(1, k + 1):
            pw[e] = pw[e - 1] * S % MOD
        # contribution: sum_j C(K,j) (-1)^j S^{K-j} P[j]
        contrib = 0
        for j in range(k + 1):
            term = comb[j] * pw[k - j] % MOD * P[j] % MOD
            if j & 1:
                contrib -= term
            else:
                contrib += term
        ans = (ans + contrib) % MOD
        # add current S into power sums
        for j in range(k + 1):
            P[j] += pw[j]
            if P[j] >= MOD:
                P[j] -= MOD

    print(ans % MOD)

main()