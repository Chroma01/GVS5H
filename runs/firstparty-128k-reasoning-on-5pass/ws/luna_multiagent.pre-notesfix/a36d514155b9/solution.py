class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 1_000_000_007
        cells = m * n

        # Compute C(cells - 2, k - 2) modulo MOD.
        limit = cells - 2
        factorial = [1] * (limit + 1)
        for i in range(1, limit + 1):
            factorial[i] = factorial[i - 1] * i % MOD

        inverse_factorial = [1] * (limit + 1)
        inverse_factorial[limit] = pow(factorial[limit], MOD - 2, MOD)
        for i in range(limit, 0, -1):
            inverse_factorial[i - 1] = inverse_factorial[i] * i % MOD

        pair_arrangements = (
            factorial[cells - 2]
            * inverse_factorial[k - 2]
            * inverse_factorial[cells - k]
        ) % MOD

        def index_pair_distance_sum(length: int) -> int:
            # Sum of (j - i) over all 0 <= i < j < length.
            return length * (length - 1) * (length + 1) // 6

        horizontal = m * m * index_pair_distance_sum(n)
        vertical = n * n * index_pair_distance_sum(m)
        all_pair_distances = (horizontal + vertical) % MOD

        return all_pair_distances * pair_arrangements % MOD