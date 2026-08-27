class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7

        total_transitions = n - 1

        fact = [1] * (total_transitions + 1)
        for i in range(1, total_transitions + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (total_transitions + 1)
        inv_fact[total_transitions] = pow(fact[total_transitions], MOD - 2, MOD)
        for i in range(total_transitions, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        combinations = (
            fact[total_transitions]
            * inv_fact[k]
            % MOD
            * inv_fact[total_transitions - k]
            % MOD
        )

        return (
            m
            * combinations
            % MOD
            * pow(m - 1, total_transitions - k, MOD)
            % MOD
        )