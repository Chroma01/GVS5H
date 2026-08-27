class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7

        # Choose which k of the n-1 adjacent gaps are equal.
        N = n - 1
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        comb = fact[N] * inv_fact[k] % MOD * inv_fact[N - k] % MOD

        # The equal gaps merge the array into n-k runs.
        # First run: m choices; each later run: m-1 choices.
        return comb * m % MOD * pow(m - 1, n - k - 1, MOD) % MOD