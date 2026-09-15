class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7

        # Invalid number of equal adjacent pairs.
        if k < 0 or k > n - 1:
            return 0

        # With only one possible value, all adjacent pairs must be equal.
        if m == 1:
            return 1 if k == n - 1 else 0

        # Choose exactly k equal adjacent positions among n - 1 positions.
        # This creates n - k runs. The first run has m choices,
        # each following run has m - 1 choices different from the previous run.
        #
        # Answer = C(n - 1, k) * m * (m - 1)^(n - k - 1) mod MOD.

        N = n - 1

        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % MOD

        invfact = [1] * (N + 1)
        invfact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N, 0, -1):
            invfact[i - 1] = invfact[i] * i % MOD

        comb = fact[N] * invfact[k] % MOD * invfact[N - k] % MOD

        return comb * (m % MOD) % MOD * pow((m - 1) % MOD, N - k, MOD) % MOD