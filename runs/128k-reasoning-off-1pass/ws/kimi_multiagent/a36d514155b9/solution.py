import math

MOD = 10**9 + 7


class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        N = m * n
        # Sum of Manhattan distances over all unordered pairs of cells:
        # row part: n^2 * sum_{i<j} (j-i) = n^2 * m(m^2-1)/6
        # col part: m^2 * n(n^2-1)/6
        row_sum = n * n * (m * (m * m - 1) // 6)
        col_sum = m * m * (n * (n * n - 1) // 6)
        total_pair_dist = row_sum + col_sum
        # Each pair of cells appears together in exactly C(N-2, k-2) arrangements
        arrangements_containing_pair = math.comb(N - 2, k - 2)
        return (total_pair_dist % MOD) * (arrangements_containing_pair % MOD) % MOD