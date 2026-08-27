class Solution:
    MOD = 10**9 + 7

    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        # Edge cases: k must be between 0 and n-1
        if k < 0 or k > n - 1:
            return 0

        # Precompute factorials up to n-1 (we need up to n-1 for combinations)
        # fac[i] = i! mod MOD
        fac = [1] * (n)
        for i in range(1, n):
            fac[i] = fac[i-1] * i % self.MOD

        # invfac[i] = (i!)^{-1} mod MOD using Fermat's little theorem
        invfac = [1] * (n)
        invfac[n-1] = pow(fac[n-1], self.MOD - 2, self.MOD)
        for i in range(n-2, -1, -1):
            invfac[i] = invfac[i+1] * (i+1) % self.MOD

        # C(n-1, k) = fac[n-1] * invfac[k] * invfac[n-1-k] % MOD
        comb = fac[n-1] * invfac[k] % self.MOD * invfac[n-1-k] % self.MOD

        # Number of runs r = n - k
        # First run: m choices, each subsequent run: (m-1) choices
        # Total runs-1 = n - k - 1
        pow_m1 = pow(m - 1, n - k - 1, self.MOD)

        result = comb * m % self.MOD * pow_m1 % self.MOD
        return result