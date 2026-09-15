class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7

        # k must be a valid number of equal adjacent pairs among n-1 gaps
        if k < 0 or k > n - 1:
            return 0

        # Precompute factorials and inverse factorials up to n-1 for binomials
        maxn = n
        fact = [1] * (maxn + 1)
        for i in range(1, maxn + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (maxn + 1)
        inv_fact[maxn] = pow(fact[maxn], MOD - 2, MOD)
        for i in range(maxn, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        def comb(a, b):
            if b < 0 or b > a:
                return 0
            return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

        # Runs decomposition: (n-1) gaps, choose k equal gaps.
        # n-k runs: first run has m choices, each later run has m-1 choices.
        # answer = m * C(n-1, k) * (m-1)^(n-1-k)
        result = m % MOD
        result = result * comb(n - 1, k) % MOD
        result = result * pow(m - 1, n - 1 - k, MOD) % MOD
        return result