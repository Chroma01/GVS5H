class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        N = m * n
        
        # Precompute factorials and inverse factorials up to N
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i-1] * i % MOD
        
        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N - 1, -1, -1):
            inv_fact[i] = inv_fact[i+1] * (i+1) % MOD
        
        def comb(n, r):
            if r < 0 or r > n:
                return 0
            return fact[n] * inv_fact[r] % MOD * inv_fact[n-r] % MOD
        
        inv6 = pow(6, MOD - 2, MOD)
        
        # Row contribution: n^2 * m*(m^2 - 1)/6
        # Using formula m^3 - m = m*(m^2 - 1)
        row_sum = (n % MOD) * (n % MOD) % MOD
        row_sum = row_sum * (m % MOD) % MOD
        row_sum = row_sum * ((m % MOD * m % MOD - 1 + MOD) % MOD) % MOD
        row_sum = row_sum * inv6 % MOD
        
        # Column contribution: m^2 * n*(n^2 - 1)/6
        col_sum = (m % MOD) * (m % MOD) % MOD
        col_sum = col_sum * (n % MOD) % MOD
        col_sum = col_sum * ((n % MOD * n % MOD - 1 + MOD) % MOD) % MOD
        col_sum = col_sum * inv6 % MOD
        
        total_pair_sum = (row_sum + col_sum) % MOD
        
        # Number of subsets of size k containing a fixed pair = C(N-2, k-2)
        c = comb(N - 2, k - 2)
        
        answer = total_pair_sum * c % MOD
        return answer