class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        N = m * n

        # S = sum over unordered pairs of cells of Manhattan distance.
        # Rows: n^2 * sum_{i<j} (j-i) = n^2 * (m-1)m(m+1)/6
        # Cols: m^2 * (n-1)n(n+1)/6
        row_sum = (m - 1) * m * (m + 1) // 6 % MOD
        col_sum = (n - 1) * n * (n + 1) // 6 % MOD
        S = (pow(n, 2, MOD) * row_sum + pow(m, 2, MOD) * col_sum) % MOD

        # factorials for C(N-2, k-2)
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        def C(a, b):
            if b < 0 or b > a or a < 0:
                return 0
            return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

        # Each unordered pair of cells appears in C(N-2, k-2) arrangements.
        return C(N - 2, k - 2) * S % MOD