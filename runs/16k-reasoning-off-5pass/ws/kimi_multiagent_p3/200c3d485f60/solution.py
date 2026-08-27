class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7

        # Precompute factorials and inverse factorials up to n-1
        fact = [1] * n
        for i in range(1, n):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * n
        inv_fact[n - 1] = pow(fact[n - 1], MOD - 2, MOD)
        for i in range(n - 2, -1, -1):
            inv_fact[i] = inv_fact[i + 1] * (i + 1) % MOD

        # C(n-1, k)
        comb = fact[n - 1] * inv_fact[k] % MOD * inv_fact[n - 1 - k] % MOD

        # m * C(n-1, k) * (m-1)^(n-1-k)
        # Note: pow(0, 0, MOD) == 1 and pow(0, positive, MOD) == 0,
        # which correctly handles m == 1 (answer is 1 iff k == n-1).
        return m % MOD * comb % MOD * pow(m - 1, n - 1 - k, MOD) % MOD