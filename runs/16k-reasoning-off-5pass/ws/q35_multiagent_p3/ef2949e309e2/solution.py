from typing import List
from collections import Counter
import math

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # Precompute combinations using Pascal's triangle or factorials
        # Since n <= 1000, we can precompute nCr for small r (up to 4)
        # Or just use math.comb which is efficient enough for small r
        
        def nCr_mod(n, r):
            if r < 0 or r > n:
                return 0
            return math.comb(n, r) % MOD

        total_ways = 0
        
        # Precompute prefix and suffix frequency maps? 
        # Actually, for each i, we can maintain left and right counts.
        # But recomputing for each i is O(N^2) which is fine for N=1000.
        
        # To optimize, we can use a single pass and update counts.
        # However, given N=1000, O(N^2) with simple loops is acceptable.
        
        # Let's precompute prefix counts and suffix counts for each value?
        # The values can be large, so we use hash maps.
        
        # Precompute prefix frequency maps
        # prefix_counts[i] is a Counter for nums[0...i-1]
        # suffix_counts[i] is a Counter for nums[i+1...n-1]
        
        prefix_counts = [Counter() for _ in range(n + 1)]
        suffix_counts = [Counter() for _ in range(n + 1)]
        
        for i in range(n):
            prefix_counts[i + 1] = prefix_counts[i].copy()
            prefix_counts[i + 1][nums[i]] += 1
            
        for i in range(n - 1, -1, -1):
            suffix_counts[i] = suffix_counts[i + 1].copy()
            suffix_counts[i][nums[i]] += 1
            
        # Now iterate over each index i as the middle element
        for i in range(n):
            v = nums[i]
            
            # Get counts from left and right
            left_map = prefix_counts[i]
            right_map = suffix_counts[i + 1]
            
            cntL_v = left_map.get(v, 0)
            cntR_v = right_map.get(v, 0)
            
            # Total elements on left and right
            totalL = i
            totalR = n - 1 - i
            
            # Non-v counts
            nonL = totalL - cntL_v
            nonR = totalR - cntR_v
            
            # Iterate over k_vL (0 to 2) and k_vR (0 to 2)
            for k_vL in range(3):
                if k_vL > cntL_v:
                    continue
                for k_vR in range(3):
                    if k_vR > cntR_v:
                        continue
                    
                    k = k_vL + k_vR
                    needL = 2 - k_vL
                    needR = 2 - k_vR
                    
                    # Calculate ways to choose v's
                    ways_v = nCr_mod(cntL_v, k_vL) * nCr_mod(cntR_v, k_vR) % MOD
                    
                    if k == 0:
                        # Total v count is 1. Need 4 non-v. 
                        # Condition: no non-v appears >= 1 time -> impossible if needL+needR > 0
                        if needL + needR > 0:
                            continue
                        else:
                            ways_non_v = 1
                    elif k == 1:
                        # Total v count is 2. Need 3 non-v.
                        # Condition: all 3 non-v must be distinct.
                        # Cases: (needL=1, needR=2) or (needL=2, needR=1)
                        if needL == 1 and needR == 2:
                            # Pick 1 from left, 2 from right, all distinct
                            # Sum over each unique value u in left:
                            # freqL[u] * C(nonR - freqR[u], 2)
                            ways_non_v = 0
                            for u, freq_u in left_map.items():
                                if u == v:
                                    continue
                                # We need to pick 2 from right that are not u and distinct
                                # Number of non-u elements in right: nonR - freqR[u]
                                rem_nonR = nonR - right_map.get(u, 0)
                                if rem_nonR >= 2:
                                    ways_non_v = (ways_non_v + freq_u * nCr_mod(rem_nonR, 2)) % MOD
                        elif needL == 2 and needR == 1:
                            # Pick 2 from left, 1 from right, all distinct
                            # Sum over each unique value w in right:
                            # freqR[w] * C(nonL - freqL[w], 2)
                            ways_non_v = 0
                            for w, freq_w in right_map.items():
                                if w == v:
                                    continue
                                rem_nonL = nonL - left_map.get(w, 0)
                                if rem_nonL >= 2:
                                    ways_non_v = (ways_non_v + freq_w * nCr_mod(rem_nonL, 2)) % MOD
                        else:
                            # Should not happen as needL+needR=3 and needL,needR in {0,1,2}
                            # Only (1,2) and (2,1) are possible for k=1
                            ways_non_v = 0
                    else:
                        # k >= 2: Total v count >= 3.
                        # Max frequency of any other value is at most 2 (if k=2) or 1 (if k=3) or 0 (if k=4).
                        # Since 1+k >= 3, and max other freq <= 2 < 3, condition always holds.
                        ways_non_v = nCr_mod(nonL, needL) * nCr_mod(nonR, needR) % MOD
                    
                    total_ways = (total_ways + ways_v * ways_non_v) % MOD
                    
        return total_ways