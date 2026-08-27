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

        pair_multiplier = (
            factorial[total_cells - 2]
            * inv_factorial[k - 2]
            % MOD
            * inv_factorial[total_cells - k]
            % MOD
        )

        def dimension_pair_sum(length: int) -> int:
            return length * (length - 1) * (length + 1) // 6

        row_distance_sum = (
            n * n * dimension_pair_sum(m)
        ) % MOD
        column_distance_sum = (
            m * m * dimension_pair_sum(n)
        ) % MOD

        return pair_multiplier * (row_distance_sum + column_distance_sum) % MOD