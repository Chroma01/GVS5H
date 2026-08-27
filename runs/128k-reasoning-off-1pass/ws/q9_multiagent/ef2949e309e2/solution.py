from typing import List
from collections import Counter

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        
        def nC2(n):
            if n < 2:
                return 0
            return n * (n - 1) // 2
        
        n = len(nums)
        total_ans = 0
        
        # right_counts will store frequencies of elements in nums[i+1:]
        # left_counts will store frequencies of elements in nums[:i]
        right_counts = Counter(nums)
        left_counts = Counter()
        
        for i in range(n):
            val = nums[i]
            
            # Remove current element from right_counts as it is the middle element
            # and not part of the right selection pool.
            right_counts[val] -= 1
            if right_counts[val] == 0:
                del right_counts[val]
            
            # Get counts for the current middle element
            cntL = left_counts.get(val, 0)
            cntR = right_counts.get(val, 0)
            
            # Total elements available in left and right pools
            totalL = i
            totalR = n - 1 - i
            
            # Non-val counts in left and right pools
            nonValL = totalL - cntL
            nonValR = totalR - cntR
            
            ways = 0
            
            # Case 1: Count(val) >= 3
            # We need to pick kL from left and kR from right such that kL + kR >= 2
            # where kL is number of 'val's picked from left, kR is number of 'val's picked from right.
            # The remaining (2 - kL) from left and (2 - kR) from right must be non-val.
            
            # (2, 0): 2 val from left, 0 val from right -> 2 non-val from right
            if cntL >= 2 and nonValR >= 2:
                ways = (ways + nC2(cntL) * nC2(nonValR)) % MOD
            
            # (1, 1): 1 val from left, 1 non-val left; 1 val from right, 1 non-val right
            if cntL >= 1 and nonValL >= 1 and cntR >= 1 and nonValR >= 1:
                ways = (ways + (cntL * nonValL) * (cntR * nonValR)) % MOD
            
            # (0, 2): 0 val from left, 2 non-val left; 2 val from right
            if nonValL >= 2 and cntR >= 2:
                ways = (ways + nC2(nonValL) * nC2(cntR)) % MOD
            
            # (2, 1): 2 val from left, 1 non-val left; 1 val from right, 1 non-val right
            if cntL >= 2 and nonValL >= 1 and cntR >= 1 and nonValR >= 1:
                ways = (ways + (nC2(cntL) * nonValL) * (cntR * nonValR)) % MOD
            
            # (1, 2): 1 val from left, 1 non-val left; 2 val from right, 1 non-val right
            if cntL >= 1 and nonValL >= 1 and cntR >= 2 and nonValR >= 1:
                ways = (ways + (cntL * nonValL) * (nC2(cntR) * nonValR)) % MOD
            
            # (2, 2): 2 val from left, 2 val from right
            if cntL >= 2 and cntR >= 2:
                ways = (ways + nC2(cntL) * nC2(cntR)) % MOD
            
            # Case 2: Count(val) == 2
            # Requires exactly 1 'val' from left and 0 from right (Total 2)
            # OR 0 from left and 1 from right (Total 2).
            # In these cases, we must ensure no other element appears twice.
            
            # Subcase 2a: 1 val from left, 1 non-val left; 0 val from right, 2 non-val right
            if cntL >= 1 and nonValL >= 1 and nonValR >= 2:
                total_ways = (cntL * nonValL) * nC2(nonValR)
                invalid = 0
                
                # Invalid if two right non-vals are the same
                # Sum C(freq_R(v), 2) for all v != val in right
                sum_C2_nonValR = 0
                for v, count in right_counts.items():
                    if v == val: continue
                    sum_C2_nonValR = (sum_C2_nonValR + nC2(count)) % MOD
                invalid = (invalid + (cntL * nonValL) * sum_C2_nonValR) % MOD
                
                # Invalid if left non-val (x) matches one of the right non-vals
                # Sum over each instance of non-val x in left: (Total pairs in right - pairs without x)
                for v, countL in left_counts.items():
                    if v == val: continue
                    freqR_v = right_counts.get(v, 0)
                    if freqR_v > 0:
                        pairs_with_x = nC2(nonValR) - nC2(nonValR - freqR_v)
                        invalid = (invalid + countL * pairs_with_x) % MOD
                
                ways = (ways + (total_ways - invalid + MOD) % MOD) % MOD
            
            # Subcase 2b: 0 val from left, 2 non-val left; 1 val from right, 1 non-val right
            if nonValL >= 2 and cntR >= 1 and nonValR >= 1:
                total_ways = nC2(nonValL) * (cntR * nonValR)
                invalid = 0
                
                # Invalid if two left non-vals are the same
                sum_C2_nonValL = 0
                for v, count in left_counts.items():
                    if v == val: continue
                    sum_C2_nonValL = (sum_C2_nonValL + nC2(count)) % MOD
                invalid = (invalid + sum_C2_nonValL * (cntR * nonValR)) % MOD
                
                # Invalid if right non-val (x) matches one of the left non-vals
                for v, countR in right_counts.items():
                    if v == val: continue
                    countL_v = left_counts.get(v, 0)
                    if countL_v > 0:
                        pairs_with_x = nC2(nonValL) - nC2(nonValL - countL_v)
                        invalid = (invalid + countR * pairs_with_x) % MOD
                
                ways = (ways + (total_ways - invalid + MOD) % MOD) % MOD
            
            total_ans = (total_ans + ways) % MOD
            
            # Update counts for next iteration
            # Move nums[i] from right to left (conceptually, it becomes part of the left pool for i+1)
            left_counts[val] = left_counts.get(val, 0) + 1
            
        return total_ans