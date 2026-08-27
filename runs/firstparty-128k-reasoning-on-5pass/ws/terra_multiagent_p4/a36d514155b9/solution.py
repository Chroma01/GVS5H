class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        total_cells = m * n

        # Sum Manhattan distances over all unordered pairs of cells.
        # Sum_{d=1}^{x-1} d * (x-d) = x * (x-1) * (x+1) / 6.
        row_gap_sum = m * (m - 1) * (m + 1) // 6
        col_gap_sum = n * (n - 1) * (n + 1) // 6

        geometry_sum = (
            row_gap_sum * n * n
            + col_gap_sum * m * m
        ) % MOD

        # Every fixed unordered pair of cells occurs in exactly
        # C(total_cells - 2, k - 2) arrangements.
        fact = [1] * (total_cells + 1)
        for i in range(1, total_cells + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (total_cells + 1)
        inv_fact[total_cells] = pow(fact[total_cells], MOD - 2, MOD)
        for i in range(total_cells, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        ways = (
            fact[total_cells - 2]
            * inv_fact[k - 2]
            % MOD
            * inv_fact[total_cells - k]
            % MOD
        )

        return geometry_sum * ways % MOD