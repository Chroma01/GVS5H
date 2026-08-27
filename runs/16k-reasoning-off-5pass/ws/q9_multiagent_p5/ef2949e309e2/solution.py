from typing import List
from collections import Counter
import math

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # Precompute prefix counts for each number
        # prefix_counts[i][val] = count of val in nums[0...i-1]
        prefix_counts = [{} for _ in range(n + 1)]
        for i in range(n):
            prefix_counts[i+1] = dict(prefix_counts[i])
            prefix_counts[i+1][nums[i]] = prefix_counts[i+1].get(nums[i], 0) + 1
            
        # Precompute suffix counts for each number
        # suffix_counts[i][val] = count of val in nums[i...n-1]
        suffix_counts = [{} for _ in range(n + 1)]
        for i in range(n - 1, -1, -1):
            suffix_counts[i] = dict(suffix_counts[i+1])
            suffix_counts[i][nums[i]] = suffix_counts[i].get(nums[i], 0) + 1
            
        # Helper to get combinations C(n, k)
        def nCr(n, r):
            if r < 0 or r > n:
                return 0
            if r == 0 or r == n:
                return 1
            if r > n // 2:
                r = n - r
            
            res = 1
            for i in range(r):
                res = res * (n - i) // (i + 1)
            return res
        
        total_ways = 0
        
        # Iterate through each element as the potential middle element
        for i in range(n):
            x = nums[i]
            left_count = prefix_counts[i].get(x, 0)
            right_count = suffix_counts[i+1].get(x, 0)
            
            left_total = i
            right_total = n - 1 - i
            
            # We need to choose 2 from left and 2 from right
            # cL: count of x from left (0, 1, 2)
            # cR: count of x from right (0, 1, 2)
            
            for cL in range(3):
                if cL > left_count or (2 - cL) > left_total:
                    continue
                ways_L = nCr(left_count, cL) * nCr(left_total - left_count, 2 - cL)
                
                for cR in range(3):
                    if cR > right_count or (2 - cR) > right_total:
                        continue
                    ways_R = nCr(right_count, cR) * nCr(right_total - right_count, 2 - cR)
                    
                    K = 1 + cL + cR
                    current_ways = ways_L * ways_R
                    
                    if K < 2:
                        continue
                    
                    if K >= 3:
                        # Unique mode guaranteed because x appears >= 3 times.
                        # The remaining 2 elements can have at most frequency 2.
                        # 3 > 2, so x is strictly the unique mode.
                        total_ways = (total_ways + current_ways) % MOD
                    else:
                        # K == 2. We need to subtract cases where another number appears 2 times.
                        # This happens if we picked exactly 1 x from one side and 0 from the other.
                        
                        if cL == 1 and cR == 0:
                            # Configuration: 1 x from Left, 1 non-x from Left, 2 from Right
                            # We need to ensure no other number y appears 2 times in the subsequence.
                            # The subsequence elements are: {x, non_x_L, y1, y2} where y1, y2 are from Right.
                            # Bad cases:
                            # 1. y1 == y2 (both from Right are same number y != x)
                            # 2. non_x_L == y1 (one from Right is same as non_x_L)
                            
                            L_non_x = left_total - left_count
                            R_total_slots = right_total
                            
                            if L_non_x == 0 or R_total_slots < 2:
                                continue
                            
                            total_ways_K2 = L_non_x * nCr(R_total_slots, 2)
                            bad_ways = 0
                            
                            # Iterate over unique numbers to find y that appears 2 times
                            unique_nums = set(prefix_counts[i].keys()) | set(suffix_counts[i+1].keys())
                            
                            for y in unique_nums:
                                if y == x:
                                    continue
                                count_y_L = prefix_counts[i].get(y, 0)
                                count_y_R = suffix_counts[i+1].get(y, 0)
                                
                                # Case 1: y appears twice in Right (y1 == y2)
                                # We need to pick 2 y's from Right.
                                # This is possible if count_y_R >= 2.
                                if count_y_R >= 2:
                                    # Ways to pick 2 y's from Right: nCr(count_y_R, 2)
                                    # The non_x_L is fixed (any of L_non_x choices)
                                    term1 = L_non_x * nCr(count_y_R, 2)
                                    bad_ways = (bad_ways + term1) % MOD
                                
                                # Case 2: y appears once in Right and matches non_x_L
                                # We need to pick 1 y from Right (count_y_R ways)
                                # And non_x_L must be y.
                                # The number of ways to pick non_x_L that is y is count_y_L.
                                # So we have count_y_L choices for non_x_L.
                                # And count_y_R choices for the y from Right.
                                # Total bad ways for this y: count_y_L * count_y_R
                                # Note: We don't multiply by anything else because the other slot in Right is filled by a non-y (implicitly handled by nCr(R_total_slots, 2) logic? No.)
                                # Let's re-derive carefully.
                                # Total ways for this branch: L_non_x * nCr(R_total_slots, 2).
                                # We are summing bad_ways.
                                # Bad case: The set {non_x_L, y1, y2} contains a duplicate y.
                                # Subcase 2a: y1 == y2 == y. (Covered above)
                                # Subcase 2b: non_x_L == y1 (and y2 != y1).
                                #   We need to choose non_x_L = y. There are count_y_L ways to pick this specific element from Left.
                                #   We need to choose y1 = y from Right. There are count_y_R ways.
                                #   We need to choose y2 from Right such that y2 != y.
                                #   Number of ways to choose y2 from Right (excluding y) = R_total_slots - count_y_R.
                                #   So term = count_y_L * count_y_R * (R_total_slots - count_y_R).
                                if count_y_L > 0 and count_y_R > 0:
                                    term2 = count_y_L * count_y_R * (R_total_slots - count_y_R)
                                    bad_ways = (bad_ways + term2) % MOD
                            
                            total_ways_K2 = (total_ways_K2 - bad_ways + MOD) % MOD
                            total_ways = (total_ways + total_ways_K2) % MOD
                            
                        elif cL == 0 and cR == 1:
                            # Configuration: 2 from Left, 1 x from Right, 1 non-x from Right
                            # Subsequence: {y1, y2, x, non_x_R}
                            # Bad cases:
                            # 1. y1 == y2 (both from Left are same number y != x)
                            # 2. non_x_R == y1 (one from Left matches non_x_R)
                            
                            L_total_slots = left_total
                            R_non_x = right_total - right_count
                            
                            if L_total_slots < 2 or R_non_x == 0:
                                continue
                            
                            total_ways_K2 = nCr(L_total_slots, 2) * R_non_x
                            bad_ways = 0
                            
                            unique_nums = set(prefix_counts[i].keys()) | set(suffix_counts[i+1].keys())
                            
                            for y in unique_nums:
                                if y == x:
                                    continue
                                count_y_L = prefix_counts[i].get(y, 0)
                                count_y_R = suffix_counts[i+1].get(y, 0)
                                
                                # Case 1: y appears twice in Left (y1 == y2)
                                if count_y_L >= 2:
                                    term1 = nCr(count_y_L, 2) * R_non_x
                                    bad_ways = (bad_ways + term1) % MOD
                                
                                # Case 2: non_x_R == y (and y1 != y2)
                                # We need to choose non_x_R = y. There are count_y_R ways.
                                # We need to choose y1 = y from Left. There are count_y_L ways.
                                # We need to choose y2 from Left such that y2 != y.
                                # Number of ways = L_total_slots - count_y_L.
                                if count_y_R > 0 and count_y_L > 0:
                                    term2 = count_y_R * count_y_L * (L_total_slots - count_y_L)
                                    bad_ways = (bad_ways + term2) % MOD
                            
                            total_ways_K2 = (total_ways_K2 - bad_ways + MOD) % MOD
                            total_ways = (total_ways + total_ways_K2) % MOD

        return total_ways