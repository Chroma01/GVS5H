class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7

        # Factorials and inverse factorials up to n-1 for binomial coefficients
        N = n - 1
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], MOD - 2, MOD)  # Fermat's little theorem
        for i in range(N, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        # C(n-1, k)
        comb = fact[N] * inv_fact[k] % MOD * inv_fact[N - k] % MOD

        # m choices for first element, (m-1) choices for each "different" gap
        ans = m % MOD
        ans = ans * pow(m - 1, N - k, MOD) % MOD
        ans = ans * comb % MOD
        return ans