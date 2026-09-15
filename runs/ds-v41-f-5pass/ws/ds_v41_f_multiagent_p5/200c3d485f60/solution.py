class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        # Precompute factorials and inverse factorials up to n
        limit = n
        fact = [1] * (limit + 1)
        for i in range(1, limit + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * (limit + 1)
        inv_fact[limit] = pow(fact[limit], MOD - 2, MOD)
        for i in range(limit, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        def comb(a, b):
            if b < 0 or b > a:
                return 0
            return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

        # Choose which of the n-1 adjacent gaps are equal
        ways = comb(n - 1, k)
        # Choose arr[0]
        ways = ways * (m % MOD) % MOD
        # Each of the n-1-k differing gaps has (m-1) choices
        ways = ways * pow((m - 1) % MOD, n - 1 - k, MOD) % MOD
        return ways