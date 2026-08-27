class Solution:
    MOD = 10**9 + 7

    def _prepare_factorials(self, N):
        # precompute factorials and inverse factorials up to N
        fact = [1] * (N + 1)
        for i in range(2, N + 1):
            fact[i] = fact[i-1] * i % self.MOD
        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], self.MOD - 2, self.MOD)
        for i in range(N, 0, -1):
            inv_fact[i-1] = inv_fact[i] * i % self.MOD
        return fact, inv_fact

    def _nCr(self, n, r, fact, inv_fact):
        if r < 0 or r > n:
            return 0
        return fact[n] * inv_fact[r] % self.MOD * inv_fact[n-r] % self.MOD

    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = self.MOD
        total_cells = m * n
        fact, inv_fact = self._prepare_factorials(total_cells)

        # Number of arrangements where a given pair of cells is both occupied
        pairs = self._nCr(total_cells - 2, k - 2, fact, inv_fact)

        # Sum of Manhattan distances over all unordered pairs of distinct cells
        # Sx = n^2 * m(m-1)(m+1)/6
        # Sy = m^2 * n(n-1)(n+1)/6
        inv6 = pow(6, MOD - 2, MOD)

        term_x = n % MOD
        term_x = term_x * term_x % MOD          # n^2
        term_x = term_x * (m % MOD) % MOD       # n^2 * m
        term_x = term_x * ((m - 1) % MOD) % MOD # n^2 * m * (m-1)
        term_x = term_x * ((m + 1) % MOD) % MOD # n^2 * m * (m-1) * (m+1)
        term_x = term_x * inv6 % MOD

        term_y = m % MOD
        term_y = term_y * term_y % MOD          # m^2
        term_y = term_y * (n % MOD) % MOD       # m^2 * n
        term_y = term_y * ((n - 1) % MOD) % MOD # m^2 * n * (n-1)
        term_y = term_y * ((n + 1) % MOD) % MOD # m^2 * n * (n-1) * (n+1)
        term_y = term_y * inv6 % MOD

        S = (term_x + term_y) % MOD
        return pairs * S % MOD