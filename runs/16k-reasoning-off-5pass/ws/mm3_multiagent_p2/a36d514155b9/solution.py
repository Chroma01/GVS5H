class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        N = m * n
        
        # Precompute factorials and inverse factorials up to N
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % MOD
        
        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N - 1, -1, -1):
            inv_fact[i] = inv_fact[i + 1] * (i + 1) % MOD
        
        def C(n, r):
            if r < 0 or r > n:
                return 0
            return fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD
        
        # Sx = n^2 * sum_{0 <= i < j < m} (j - i) = n^2 * m*(m^2-1)/6
        inv6 = pow(6, MOD - 2, MOD)
        Sx = n * n % MOD * m % MOD * ((m * m - 1) % MOD) % MOD * inv6 % MOD
        # Sy = m^2 * n*(n^2-1)/6
        Sy = m * m % MOD * n % MOD * ((n * n - 1) % MOD) % MOD * inv6 % MOD
        
        total_pair_sum = (Sx + Sy) % MOD
        
        # Probability that a given pair is both chosen = C(N-2, k-2) / C(N, k)
        num = C(N - 2, k - 2)
        den = C(N, k)
        fraction = num * pow(den, MOD - 2, MOD) % MOD
        
        return total_pair_sum * fraction % MOD