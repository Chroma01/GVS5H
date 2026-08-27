class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        total_cells = m * n

        factorial = [1] * (total_cells + 1)
        for i in range(1, total_cells + 1):
            factorial[i] = factorial[i - 1] * i % MOD

        inv_factorial = [1] * (total_cells + 1)
        inv_factorial[total_cells] = pow(factorial[total_cells], MOD - 2, MOD)
        for i in range(total_cells, 0, -1):
            inv_factorial[i - 1] = inv_factorial[i] * i % MOD

        arrangements_per_pair = (
            factorial[total_cells - 2]
            * inv_factorial[k - 2]
            % MOD
            * inv_factorial[total_cells - k]
            % MOD
        )

        row_distance_sum = n * n * m * (m - 1) * (m + 1) // 6
        col_distance_sum = m * m * n * (n - 1) * (n + 1) // 6

        total_pair_distance = (row_distance_sum + col_distance_sum) % MOD
        return total_pair_distance * arrangements_per_pair % MOD