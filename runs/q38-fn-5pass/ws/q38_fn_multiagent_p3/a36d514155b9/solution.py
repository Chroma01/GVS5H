class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 1_000_000_007
        total_cells = m * n

        if k < 2 or total_cells < 2 or k > total_cells:
            return 0

        # Number of arrangements containing any fixed unordered pair of cells:
        # choose the remaining k - 2 pieces from total_cells - 2 cells.
        max_fact = total_cells - 2

        fact = [1] * (max_fact + 1)
        for i in range(1, max_fact + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (max_fact + 1)
        inv_fact[max_fact] = pow(fact[max_fact], MOD - 2, MOD)
        for i in range(max_fact, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        def comb(a: int, b: int) -> int:
            if b < 0 or b > a:
                return 0
            return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

        ways = comb(total_cells - 2, k - 2)

        # Sum of Manhattan distances over all unordered pairs of grid cells.
        # Row contribution:
        #   n^2 * sum_{d=1}^{m-1} d * (m - d)
        # = n^2 * m * (m^2 - 1) / 6
        #
        # Column contribution:
        #   m^2 * sum_{d=1}^{n-1} d * (n - d)
        # = m^2 * n * (n^2 - 1) / 6
        inv6 = pow(6, MOD - 2, MOD)

        mm = m % MOD
        nn = n % MOD

        row_factor = mm * ((mm * mm - 1) % MOD) % MOD
        row_factor = row_factor * inv6 % MOD
        row_sum = nn * nn % MOD * row_factor % MOD

        col_factor = nn * ((nn * nn - 1) % MOD) % MOD
        col_factor = col_factor * inv6 % MOD
        col_sum = mm * mm % MOD * col_factor % MOD

        return ways * ((row_sum + col_sum) % MOD) % MOD