class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7

        limit = n - 1
        fact = [1] * (limit + 1)
        for i in range(1, limit + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (limit + 1)
        inv_fact[limit] = pow(fact[limit], MOD - 2, MOD)
        for i in range(limit, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        combinations = (
            fact[limit]
            * inv_fact[k]
            % MOD
            * inv_fact[limit - k]
            % MOD
        )

        return (
            m
            * combinations
            % MOD
            * pow(m - 1, limit - k, MOD)
            % MOD
        )