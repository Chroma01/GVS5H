class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        total = m * n

        # Factorials and inverse factorials up to total for binomial coefficients
        fact = [1] * (total + 1)
        for i in range(1, total + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * (total + 1)
        inv_fact[total] = pow(fact[total], MOD - 2, MOD)
        for i in range(total, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        def comb(N: int, K: int) -> int:
            if K < 0 or K > N:
                return 0
            return fact[N] * inv_fact[K] % MOD * inv_fact[N - K] % MOD

        # Number of arrangements containing any fixed pair of cells
        ways = comb(total - 2, k - 2)

        # Sum of Manhattan distances over all unordered pairs of cells:
        # x-part: n^2 * sum_{d=1}^{m-1} d*(m-d) = n^2 * m*(m^2-1)/6
        # y-part: m^2 * n*(n^2-1)/6
        inv6 = pow(6, MOD - 2, MOD)
        x_part = n * n % MOD * (m * (m * m - 1) % MOD) % MOD
        y_part = m * m % MOD * (n * (n * n - 1) % MOD) % MOD
        S = (x_part + y_part) % MOD * inv6 % MOD

        return ways * S % MOD