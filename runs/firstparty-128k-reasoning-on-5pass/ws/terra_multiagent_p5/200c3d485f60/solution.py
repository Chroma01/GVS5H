class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7

        fact = [1] * n
        inv_fact = [1] * n

        for i in range(1, n):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact[n - 1] = pow(fact[n - 1], MOD - 2, MOD)
        for i in range(n - 1, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        choose = fact[n - 1] * inv_fact[k] % MOD
        choose = choose * inv_fact[n - 1 - k] % MOD

        changes = n - 1 - k
        return choose * (m % MOD) % MOD * pow(m - 1, changes, MOD) % MOD