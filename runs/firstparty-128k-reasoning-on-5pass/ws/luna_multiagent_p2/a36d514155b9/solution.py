class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        cells = m * n

        factorial = [1] * (cells + 1)
        for i in range(1, cells + 1):
            factorial[i] = factorial[i - 1] * i % MOD

        inverse_factorial = [1] * (cells + 1)
        inverse_factorial[cells] = pow(factorial[cells], MOD - 2, MOD)
        for i in range(cells, 0, -1):
            inverse_factorial[i - 1] = (
                inverse_factorial[i] * i
            ) % MOD

        arrangements_per_pair = (
            factorial[cells - 2]
            * inverse_factorial[k - 2]
            % MOD
            * inverse_factorial[cells - k]
            % MOD
        )

        inv6 = pow(6, MOD - 2, MOD)

        row_distance_sum = (
            m * (m - 1) % MOD * (m + 1) % MOD * inv6
        ) % MOD
        column_distance_sum = (
            n * (n - 1) % MOD * (n + 1) % MOD * inv6
        ) % MOD

        total_pair_distance = (
            n * n % MOD * row_distance_sum
            + m * m % MOD * column_distance_sum
        ) % MOD

        return total_pair_distance * arrangements_per_pair % MOD