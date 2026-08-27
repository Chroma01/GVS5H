from typing import List
from collections import defaultdict

MOD = 10**9 + 7

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        n = len(nums)
        if n < 5:
            return 0
        
        # Precompute prefix and suffix frequency maps
        # prefix[i][v] = count of v in nums[0..i-1]
        # suffix[i][v] = count of v in nums[i+1..n-1]
        prefix = [defaultdict(int) for _ in range(n + 1)]
        suffix = [defaultdict(int) for _ in range(n + 1)]
        
        for i in range(n):
            for k, v in prefix[i].items():
                prefix[i+1][k] = v
            prefix[i+1][nums[i]] += 1
        
        for i in range(n-1, -1, -1):
            for k, v in suffix[i+1].items():
                suffix[i][k] = v
            suffix[i][nums[i]] += 1
        
        def C2(x):
            if x < 2:
                return 0
            return x * (x - 1) // 2
        
        ans = 0
        for m in range(n):
            L_size = m
            R_size = n - 1 - m
            T = C2(L_size) * C2(R_size) % MOD
            
            if T == 0:
                continue
            
            M = nums[m]
            cL_map = prefix[m]
            cR_map = suffix[m+1]
            
            # Get all distinct values other than M
            # We can iterate over the union of keys in cL_map and cR_map
            values = set(cL_map.keys()) | set(cR_map.keys())
            
            S_L = 0  # sum_{v != M} C(cL_v, 2)
            S_R = 0  # sum_{v != M} C(cR_v, 2)
            
            A = 0  # |A|
            B = 0  # |B|
            C = 0  # |C|
            AC = 0 # |A ∩ C|
            BC = 0 # |B ∩ C|
            ABC = 0 # |A ∩ B ∩ C|
            
            for v in values:
                if v == M:
                    continue
                cL = cL_map[v]
                cR = cR_map[v]
                
                cL2 = C2(cL)
                cR2 = C2(cR)
                
                S_L = (S_L + cL2) % MOD
                S_R = (S_R + cR2) % MOD
                
                A = (A + cL2 * C2(R_size)) % MOD
                B = (B + C2(L_size) * cR2) % MOD
                
                # |C_v| = T - C(L - cL, 2)*C(R, 2) - C(L, 2)*C(R - cR, 2) + C(L - cL, 2)*C(R - cR, 2)
                term_C = (T 
                          - C2(L_size - cL) * C2(R_size) 
                          - C2(L_size) * C2(R_size - cR) 
                          + C2(L_size - cL) * C2(R_size - cR)) % MOD
                C = (C + term_C) % MOD
                
                # |A ∩ C|: sum C(cL_v, 2) * (C(R, 2) - C(R - cR_v, 2))
                term_AC = cL2 * (C2(R_size) - C2(R_size - cR))
                AC = (AC + term_AC) % MOD
                
                # |B ∩ C|: sum C(cR_v, 2) * (C(L, 2) - C(L - cL_v, 2))
                term_BC = cR2 * (C2(L_size) - C2(L_size - cL))
                BC = (BC + term_BC) % MOD
                
                # |A ∩ B ∩ C|: sum C(cL_v, 2) * C(cR_v, 2)
                ABC = (ABC + cL2 * cR2) % MOD
            
            # |A ∩ B| = S_L * S_R
            AB = (S_L * S_R) % MOD
            
            Bad = (A + B + C - AB - AC - BC + ABC) % MOD
            Valid = (T - Bad) % MOD
            ans = (ans + Valid) % MOD
            
        return ans % MOD