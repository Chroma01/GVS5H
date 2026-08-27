class Solution:
    MOD = 10**9 + 7

    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = self.MOD
        total_cells = m * n

        # Precompute factorials and inverse factorials up to total_cells
        fact = [1] * (total_cells + 1)
        for i in range(1, total_cells + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * (total_cells + 1)
        inv_fact[total_cells] = pow(fact[total_cells], MOD - 2, MOD)
        for i in range(total_cells, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        def comb(N: int, K: int) -> int:
            if K < 0 or K > N:
                return 0
            return fact[N] * inv_fact[K] % MOD * inv_fact[N - K] % MOD

        # Number of arrangements containing any fixed pair of distinct cells
        ways = comb(total_cells - 2, k - 2)

        inv6 = pow(6, MOD - 2, MOD)

        # Sum of |r1 - r2| over all unordered pairs of cells:
        # n^2 * sum_{d=1}^{m-1} d*(m-d) = n^2 * m*(m^2-1)/6
        row_sum = n * n % MOD * m % MOD * ((m * m - 1) % MOD) % MOD * inv6 % MOD
        # Column part: m^2 * n*(n^2-1)/6
        col_sum = m * m % MOD * n % MOD * ((n * n - 1) % MOD) % MOD * inv6 % MOD

        return ways * ((row_sum + col_sum) % MOD) % MOD