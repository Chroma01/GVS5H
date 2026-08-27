class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        transitions = n - 1

        fact = [1] * (transitions + 1)
        for i in range(1, transitions + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (transitions + 1)
        inv_fact[transitions] = pow(fact[transitions], MOD - 2, MOD)
        for i in range(transitions, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        comb = fact[transitions] * inv_fact[k] % MOD
        comb = comb * inv_fact[transitions - k] % MOD

        return m * comb % MOD * pow(m - 1, transitions - k, MOD) % MOD