class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7

        if k < 0 or k > n - 1:
            return 0

        r = n - 1

        fact = [1] * (r + 1)
        for i in range(1, r + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (r + 1)
        inv_fact[r] = pow(fact[r], MOD - 2, MOD)
        for i in range(r, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        comb = fact[r] * inv_fact[k] % MOD * inv_fact[r - k] % MOD

        return comb * (m % MOD) % MOD * pow((m - 1) % MOD, r - k, MOD) % MOD