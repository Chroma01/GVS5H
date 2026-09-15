class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7

        if k < 0 or k > n - 1:
            return 0

        N = n - 1

        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        choose = fact[N] * inv_fact[k] % MOD * inv_fact[N - k] % MOD
        return choose * m % MOD * pow(m - 1, N - k, MOD) % MOD