class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        total_cells = m * n

        fact = [1] * (total_cells + 1)
        for i in range(1, total_cells + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact_k2 = pow(fact[k - 2], MOD - 2, MOD)
        inv_fact_rest = pow(fact[total_cells - k], MOD - 2, MOD)
        arrangements_per_pair = (
            fact[total_cells - 2] * inv_fact_k2 % MOD * inv_fact_rest
        ) % MOD

        row_distance_sum = (
            n * n * m * (m - 1) * (m + 1) // 6
        )
        column_distance_sum = (
            m * m * n * (n - 1) * (n + 1) // 6
        )

        total_pair_distance = (row_distance_sum + column_distance_sum) % MOD
        return total_pair_distance * arrangements_per_pair % MOD