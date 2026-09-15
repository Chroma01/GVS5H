class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        total_cells = m * n
        max_n = total_cells - 2

        # Factorials for C(total_cells - 2, k - 2) modulo MOD.
        fact = [1] * (max_n + 1)
        for i in range(1, max_n + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (max_n + 1)
        inv_fact[max_n] = pow(fact[max_n], MOD - 2, MOD)
        for i in range(max_n, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        def comb(a: int, b: int) -> int:
            if b < 0 or b > a:
                return 0
            return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

        # Every fixed unordered pair of cells appears together in exactly
        # C(total_cells - 2, k - 2) valid arrangements.
        ways = comb(total_cells - 2, k - 2)

        # Sum over all unordered row pairs of their distance:
        # 1 + 2 + ... + (L - 1) weighted by multiplicities = L * (L^2 - 1) / 6.
        inv6 = pow(6, MOD - 2, MOD)
        m_mod = m % MOD
        n_mod = n % MOD

        row_sum = m_mod * ((m_mod * m_mod - 1) % MOD) % MOD
        row_sum = row_sum * inv6 % MOD

        col_sum = n_mod * ((n_mod * n_mod - 1) % MOD) % MOD
        col_sum = col_sum * inv6 % MOD

        # Row distances are multiplied by n^2 cell choices,
        # column distances by m^2 cell choices.
        total_geom = (
            n_mod * n_mod % MOD * row_sum
            + m_mod * m_mod % MOD * col_sum
        ) % MOD

        return ways * total_geom % MOD


if __name__ == "__main__":
    sol = Solution()
    assert sol.distanceSum(2, 2, 2) == 8
    assert sol.distanceSum(1, 4, 3) == 20