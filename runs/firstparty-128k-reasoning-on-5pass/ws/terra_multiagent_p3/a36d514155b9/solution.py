class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        total_cells = m * n

        fact = [1] * (total_cells + 1)
        for i in range(1, total_cells + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (total_cells + 1)
        inv_fact[total_cells] = pow(fact[total_cells], MOD - 2, MOD)
        for i in range(total_cells, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        def comb(a, b):
            if b < 0 or b > a:
                return 0
            return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

        # Sum_{0 <= i < j < length} (j - i) = length * (length^2 - 1) / 6
        row_distance_sum = m * (m * m - 1) // 6
        col_distance_sum = n * (n * n - 1) // 6

        # Each row pair has n^2 cell pairs; each column pair has m^2 cell pairs.
        all_cell_pair_distances = (
            row_distance_sum * n * n +
            col_distance_sum * m * m
        ) % MOD

        # Every fixed unordered pair of cells is included in C(m*n-2, k-2) placements.
        arrangements_per_pair = comb(total_cells - 2, k - 2)

        return all_cell_pair_distances * arrangements_per_pair % MOD