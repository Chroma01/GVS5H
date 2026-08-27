class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 1_000_000_007
        transitions = n - 1

        fact = [1] * (transitions + 1)
        for i in range(1, transitions + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (transitions + 1)
        inv_fact[transitions] = pow(fact[transitions], MOD - 2, MOD)
        for i in range(transitions, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        combinations = (
            fact[transitions]
            * inv_fact[k]
            % MOD
            * inv_fact[transitions - k]
            % MOD
        )

        return m * combinations % MOD * pow(m - 1, transitions - k, MOD) % MOD