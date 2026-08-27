class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Helper function to compute nCr mod p
        def nCr_mod(n, r, mod):
            if r < 0 or r > n:
                return 0
            if r == 0 or r == n:
                return 1
            if r > n // 2:
                r = n - r
            
            # We need to compute n! / (r! * (n-r)!) mod mod
            # Since mod is prime, we can use Fermat's little theorem for division
            # Precompute factorials and inverse factorials if needed, but for single call:
            # Given constraints n <= 10^5, we can compute directly
            
            num = 1
            den = 1
            for i in range(r):
                num = (num * (n - i)) % mod
                den = (den * (i + 1)) % mod
            
            # Modular inverse of den
            den_inv = pow(den, mod - 2, mod)
            return (num * den_inv) % mod
        
        total_cells = m * n
        
        # Number of arrangements where two specific cells are occupied
        # C(total_cells - 2, k - 2)
        if k < 2:
            return 0
        comb = nCr_mod(total_cells - 2, k - 2, MOD)
        
        # Function to compute sum of absolute differences for all unordered pairs in 1D of length L
        def sum_1d(L):
            # Sum_{i=0}^{L-1} i * (L - 1 - i)
            # This equals: (L-1)*sum(i) - sum(i^2) for i from 0 to L-1
            # sum(i) = L*(L-1)//2
            # sum(i^2) = (L-1)*L*(2*L-1)//6
            # But we can also derive a closed form:
            # sum_{i=0}^{L-1} i*(L-1-i) = (L-1)*L*(L+1)//6 - wait, let's verify:
            # For L=1: 0
            # For L=2: 0*1 + 1*0 = 0? No, for L=2, indices 0,1: |0-1|=1, so sum=1.
            # Formula: i*(L-1-i) for i=0: 0*(1)=0, i=1: 1*0=0 -> sum=0. That's wrong.
            # Actually, the contribution of index i is: it is larger than i indices (0..i-1) and smaller than (L-1-i) indices (i+1..L-1).
            # So it contributes i * (L-1-i) to the sum of absolute differences? 
            # Let's check L=3: indices 0,1,2.
            # Pairs: (0,1):1, (0,2):2, (1,2):1. Sum=4.
            # Using formula: 
            # i=0: 0*(2)=0
            # i=1: 1*(1)=1
            # i=2: 2*(0)=0
            # Sum=1. Wrong.
            #
            # Correct approach: 
            # The sum of |i-j| for all 0<=i<j<L is:
            # = sum_{i=0}^{L-1} sum_{j=i+1}^{L-1} (j-i)
            # = sum_{d=1}^{L-1} d * (L - d)   [because for difference d, there are L-d pairs]
            #
            # Let's use this formula: sum_{d=1}^{L-1} d*(L-d)
            # = L * sum_{d=1}^{L-1} d - sum_{d=1}^{L-1} d^2
            # = L * (L-1)*L//2 - (L-1)*L*(2*L-1)//6
            # = (L^2*(L-1))//2 - (L*(L-1)*(2*L-1))//6
            # = L*(L-1) * [ L/2 - (2*L-1)/6 ]
            # = L*(L-1) * [ (3L - (2L-1)) / 6 ]
            # = L*(L-1) * (L+1) / 6
            # = L*(L^2 - 1) // 6
            
            if L < 2:
                return 0
            # Compute L*(L^2-1)//6 mod MOD
            # Since we are doing integer division, we need to be careful with mod.
            # But L*(L^2-1) is always divisible by 6.
            # We can compute it in integers then mod, since L <= 10^5, L^3 ~ 1e15 which fits in Python int.
            val = L * (L * L - 1) // 6
            return val % MOD
        
        sum_x = sum_1d(m)
        sum_y = sum_1d(n)
        
        # Total sum of Manhattan distances over all unordered pairs of cells
        # = n * sum_x + m * sum_y
        total_manhattan_sum = (n * sum_x + m * sum_y) % MOD
        
        result = (comb * total_manhattan_sum) % MOD
        return result