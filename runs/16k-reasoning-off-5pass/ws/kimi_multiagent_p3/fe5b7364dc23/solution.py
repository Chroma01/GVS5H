import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:2 + n]))

    # Binomial coefficients C(k, t) mod MOD via Pascal's rule
    C = [[0] * (k + 1) for _ in range(k + 1)]
    for i in range(k + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD

    # pw[m] = sum of S_i^m over all processed prefix sums (i < current r)
    # Initialize with S_0 = 0: 0^0 = 1, 0^m = 0 for m >= 1
    pw = [0] * (k + 1)
    pw[0] = 1

    ans = 0
    s = 0  # current prefix sum S_r
    for v in a:
        s = (s + v) % MOD

        # Compute s^t for t = 0..k
        sp = [1] * (k + 1)
        for t in range(1, k + 1):
            sp[t] = sp[t - 1] * s % MOD

        # (S_r - S_i)^k = sum_t C(k,t) S_r^t (-1)^(k-t) S_i^(k-t)
        for t in range(k + 1):
            term = C[k][t] * sp[t] % MOD * pw[k - t] % MOD
            if (k - t) & 1:
                ans = (ans - term) % MOD
            else:
                ans = (ans + term) % MOD

        # Add current S_r to the power sums
        for m in range(k + 1):
            pw[m] = (pw[m] + sp[m]) % MOD

    print(ans % MOD)

main()