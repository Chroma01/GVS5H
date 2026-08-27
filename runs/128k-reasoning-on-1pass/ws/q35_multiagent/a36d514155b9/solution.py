class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        N = m * n
        
        # Sum of Manhattan distances between all distinct pairs of cells in the grid
        # Formula: N * (m + n) * (N - 1) / 6
        inv6 = pow(6, MOD - 2, MOD)
        S = (N % MOD) * ((m + n) % MOD) % MOD
        S = S * ((N - 1) % MOD) % MOD
        S = S * inv6 % MOD
        
        # Each specific pair of cells appears in exactly binom(N-2, k-2) valid arrangements
        r = k - 2
        n_comb = N - 2
        
        if r < 0 or r > n_comb:
            C = 0
        else:
            # Compute binom(n_comb, r) mod MOD efficiently
            if r > n_comb // 2:
                r = n_comb - r
            
            num = 1
            den = 1
            for i in range(1, r + 1):
                num = num * (n_comb - i + 1) % MOD
                den = den * i % MOD
            C = num * pow(den, MOD - 2, MOD) % MOD
            
        return S * C % MOD