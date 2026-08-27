class Solution:
    MOD = 10**9 + 7

    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = self.MOD
        # Precompute factorials and inverse factorials up to n-1
        N = n - 1
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        # C(n-1, k)
        comb = fact[N] * inv_fact[k] % MOD * inv_fact[N - k] % MOD

        # ans = C(n-1, k) * m * (m-1)^(n-1-k)
        ans = comb * m % MOD
        ans = ans * pow(m - 1, N - k, MOD) % MOD
        return ans