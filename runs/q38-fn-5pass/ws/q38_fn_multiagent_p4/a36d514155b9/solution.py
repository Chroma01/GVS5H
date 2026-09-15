class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7

        total_cells = m * n
        top = total_cells - 2
        bottom = k - 2

        if bottom < 0 or bottom > top:
            return 0

        def line_pair_sum(length: int) -> int:
            # sum_{d=1}^{length-1} d * (length - d)
            # = length * (length - 1) * (length + 1) / 6
            return (length * (length - 1) * (length + 1) // 6) % MOD

        # Total Manhattan distance over all unordered pairs of cells.
        # Row contribution: n^2 * sum_d d*(m-d)
        # Column contribution: m^2 * sum_d d*(n-d)
        total_distance = (
            (n % MOD) * (n % MOD) % MOD * line_pair_sum(m)
            + (m % MOD) * (m % MOD) % MOD * line_pair_sum(n)
        ) % MOD

        # Each unordered pair of cells appears in C(total_cells - 2, k - 2)
        # valid arrangements.
        fact = [1] * (top + 1)
        for i in range(1, top + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (top + 1)
        inv_fact[top] = pow(fact[top], MOD - 2, MOD)
        for i in range(top, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        ways = fact[top] * inv_fact[bottom] % MOD * inv_fact[top - bottom] % MOD

        return total_distance * ways % MOD