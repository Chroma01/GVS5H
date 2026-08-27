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

        pair_inclusions = comb(total_cells - 2, k - 2)
        inv6 = pow(6, MOD - 2, MOD)

        row_distance_sum = (
            m % MOD
            * ((m * m - 1) % MOD)
            % MOD
            * inv6
            % MOD
            * (n * n % MOD)
            % MOD
        )

        column_distance_sum = (
            n % MOD
            * ((n * n - 1) % MOD)
            % MOD
            * inv6
            % MOD
            * (m * m % MOD)
            % MOD
        )

        return (row_distance_sum + column_distance_sum) % MOD * pair_inclusions % MOD