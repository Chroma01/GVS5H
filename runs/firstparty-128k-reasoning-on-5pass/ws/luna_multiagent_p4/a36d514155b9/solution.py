class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        cells = m * n

        row_sum = n * n * m * (m - 1) * (m + 1) // 6
        col_sum = m * m * n * (n - 1) * (n + 1) // 6
        total_pair_distance = (row_sum + col_sum) % MOD

        total_remaining = cells - 2
        selected_remaining = k - 2
        selected_remaining = min(
            selected_remaining,
            total_remaining - selected_remaining
        )

        numerator = 1
        denominator = 1
        for i in range(1, selected_remaining + 1):
            numerator = numerator * (total_remaining - selected_remaining + i) % MOD
            denominator = denominator * i % MOD

        arrangements_per_pair = (
            numerator * pow(denominator, MOD - 2, MOD)
        ) % MOD

        return total_pair_distance * arrangements_per_pair % MOD