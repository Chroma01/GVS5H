class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 1_000_000_007

        if n <= 0:
            return 0
        if k < 0 or k > n - 1:
            return 0
        if m <= 0:
            return 0

        # With only one possible value, all adjacent pairs are equal.
        if m == 1:
            return 1 if k == n - 1 else 0

        N = n - 1

        # Precompute factorials up to N.
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % MOD

        # Precompute inverse factorials up to N.
        invfact = [1] * (N + 1)
        invfact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N, 0, -1):
            invfact[i - 1] = invfact[i] * i % MOD

        # C(N, k)
        comb = fact[N] * invfact[k] % MOD * invfact[N - k] % MOD

        # Number of runs is n - k, so the power exponent is n - k - 1 = N - k.
        ans = comb * (m % MOD) % MOD
        ans = ans * pow((m - 1) % MOD, N - k, MOD) % MOD

        return ans