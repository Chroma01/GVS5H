import sys

MOD = 998244353

def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # prefix sums modulo MOD, include P0 = 0
    pref = [0] * (N + 1)
    for i in range(1, N + 1):
        pref[i] = (pref[i - 1] + A[i - 1]) % MOD

    # power_sum[m] = sum_{i=0..N} pref[i]^m  (m = 0..K)
    power_sum = [0] * (K + 1)
    # P0 = 0: 0^0 = 1, 0^m = 0 for m>0
    power_sum[0] = 1  # from P0
    # The loop will add contributions from P0 for m>0 as 0, so fine.
    for x in pref[1:]:
        # add x^0 = 1
        power_sum[0] = (power_sum[0] + 1) % MOD
        cur = 1
        for m in range(1, K + 1):
            cur = (cur * x) % MOD
            power_sum[m] = (power_sum[m] + cur) % MOD

    # precompute binomial coefficients C(K, t) for t=0..K
    comb = [[0] * (K + 1) for _ in range(K + 1)]
    for i in range(K + 1):
        comb[i][0] = comb[i][i] = 1
        for j in range(1, i):
            comb[i][j] = (comb[i - 1][j - 1] + comb[i - 1][j]) % MOD

    inv2 = (MOD + 1) // 2  # modular inverse of 2 mod MOD (since MOD is prime)
    ans = 0
    for t in range(K + 1):
        # C_t = sum_{i<j} P_i^{K-t} P_j^t
        # = ( (sum P_i^t) * (sum P_i^{K-t}) - sum P_i^K ) / 2
        sum_t = power_sum[t]
        sum_Kt = power_sum[K - t]
        sum_K = power_sum[K]
        Ct = (sum_t * sum_Kt - sum_K) % MOD
        Ct = (Ct * inv2) % MOD

        sign = 1 if (K - t) % 2 == 0 else -1
        term = comb[K][t] * Ct % MOD
        if sign == 1:
            ans = (ans + term) % MOD
        else:
            ans = (ans - term) % MOD

    print(ans % MOD)


if __name__ == "__main__":
    solve()