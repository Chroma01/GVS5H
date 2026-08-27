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

        def comb(a: int, b: int) -> int:
            if b < 0 or b > a:
                return 0
            return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

        # Sum of |i-j| over all unordered pairs of positions in one dimension.
        # sum_{d=1}^{L-1} d * (L-d) = L * (L-1) * (L+1) / 6.
        inv6 = pow(6, MOD - 2, MOD)

        def one_dim_sum(length: int) -> int:
            return length * (length - 1) % MOD * (length + 1) % MOD * inv6 % MOD

        # For row differences, independently choose a column for each endpoint: n^2 choices.
        # For column differences, independently choose a row for each endpoint: m^2 choices.
        cell_pair_distance_sum = (
            one_dim_sum(m) * n % MOD * n
            + one_dim_sum(n) * m % MOD * m
        ) % MOD

        # Every fixed unordered pair of cells occurs in C(m*n-2, k-2) arrangements.
        arrangements_per_pair = comb(total_cells - 2, k - 2)

        return cell_pair_distance_sum * arrangements_per_pair % MOD