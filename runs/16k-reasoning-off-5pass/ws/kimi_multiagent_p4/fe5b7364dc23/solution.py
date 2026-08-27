import sys

def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    a = data[2:2 + n]

    # Binomial coefficients C(k, t) for t = 0..k (k <= 10, compute directly)
    C = [1] * (k + 1)
    for t in range(1, k + 1):
        C[t] = C[t - 1] * (k - t + 1) // t

    # P[m] = sum of S_i^m over all previous prefix sums S_i (i < j)
    # Initialize with S_0 = 0: P[0] = 1, P[m] = 0 for m >= 1
    P = [0] * (k + 1)
    P[0] = 1

    ans = 0
    s = 0  # current prefix sum S_j mod MOD
    for idx in range(n):
        s = (s + int(a[idx])) % MOD

        # powers of s: sp[t] = s^t
        sp = [1] * (k + 1)
        for t in range(1, k + 1):
            sp[t] = sp[t - 1] * s % MOD

        # (S_j - S_i)^k = sum_t C(k,t) * S_j^t * (-S_i)^(k-t)
        # sum over previous i: sum_t C(k,t) * (-1)^(k-t) * s^t * P[k-t]
        contrib = 0
        for t in range(k + 1):
            term = C[t] * sp[t] % MOD * P[k - t] % MOD
            if (k - t) & 1:
                contrib -= term
            else:
                contrib += term
        ans = (ans + contrib) % MOD

        # add current prefix sum into power sums
        for m in range(k + 1):
            P[m] = (P[m] + sp[m]) % MOD

    print(ans % MOD)

main()