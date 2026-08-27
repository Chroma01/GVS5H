class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 1_000_000_007
        total_cells = m * n

        fact = [1] * (total_cells + 1)
        for i in range(1, total_cells + 1):
            fact[i] = fact[i - 1] * i % MOD

        invfact = [1] * (total_cells + 1)
        invfact[total_cells] = pow(fact[total_cells], MOD - 2, MOD)
        for i in range(total_cells, 0, -1):
            invfact[i - 1] = invfact[i] * i % MOD

        def comb(a: int, b: int) -> int:
            if b < 0 or b > a:
                return 0
            return fact[a] * invfact[b] % MOD * invfact[a - b] % MOD

        inv6 = pow(6, MOD - 2, MOD)

        def sum1d(length: int) -> int:
            x = length % MOD
            return x * ((x * x - 1) % MOD) % MOD * inv6 % MOD

        row_part = (n % MOD) * (n % MOD) % MOD * sum1d(m) % MOD
        col_part = (m % MOD) * (m % MOD) % MOD * sum1d(n) % MOD
        geometric_sum = (row_part + col_part) % MOD

        return comb(total_cells - 2, k - 2) * geometric_sum % MOD