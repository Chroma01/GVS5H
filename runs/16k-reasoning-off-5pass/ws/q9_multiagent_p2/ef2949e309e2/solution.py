from typing import List
from collections import Counter
from math import comb

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        if n < 5:
            return 0
        
        ans = 0
        
        # Precompute factorials and inverse factorials for combinations to avoid repeated math.comb calls
        # Although math.comb is efficient, for N=1000 and O(N^2) complexity, precomputing is safer and cleaner.
        # However, since we only need small combinations (k <= 2), math.comb is perfectly fine and fast.
        # We will use math.comb directly.
        
        for i in range(n):
            val = nums[i]
            
            # Count occurrences of val and non-val in left and right parts
            left_val = 0
            right_val = 0
            left_non = 0
            right_non = 0
            
            # Frequency maps for left and right excluding val
            left_counts = Counter()
            right_counts = Counter()
            
            # Build counts for left part (indices 0 to i-1)
            for j in range(i):
                if nums[j] == val:
                    left_val += 1
                else:
                    left_counts[nums[j]] += 1
                    left_non += 1
            
            # Build counts for right part (indices i+1 to n-1)
            for j in range(i+1, n):
                if nums[j] == val:
                    right_val += 1
                else:
                    right_counts[nums[j]] += 1
                    right_non += 1
            
            # Helper to get combinations
            def get_comb(n, k):
                if k < 0 or k > n:
                    return 0
                return comb(n, k)
            
            ways_k_ge_3 = 0
            
            # Case 1: k >= 3 (val appears 3 or 4 times in subsequence)
            # We need to pick 2 more val's from left+right such that total val count >= 3.
            # Since we already have 1 val at index i, we need at least 2 more.
            # Possible splits (left_val_picked, right_val_picked): (2, 0), (1, 1), (0, 2)
            # The remaining slots must be filled with non-val elements.
            
            # Split (2, 0): Pick 2 val from left, 0 from right
            # Then we need 0 non-val from left, 2 non-val from right
            if left_val >= 2 and right_non >= 2:
                ways = get_comb(left_val, 2) * get_comb(right_val, 0) * get_comb(left_non, 0) * get_comb(right_non, 2)
                ways_k_ge_3 = (ways_k_ge_3 + ways) % MOD
            
            # Split (1, 1): Pick 1 val from left, 1 from right
            # Then we need 1 non-val from left, 1 non-val from right
            if left_val >= 1 and right_val >= 1 and left_non >= 1 and right_non >= 1:
                ways = get_comb(left_val, 1) * get_comb(right_val, 1) * get_comb(left_non, 1) * get_comb(right_non, 1)
                ways_k_ge_3 = (ways_k_ge_3 + ways) % MOD
            
            # Split (0, 2): Pick 0 val from left, 2 from right
            # Then we need 2 non-val from left, 0 from right
            if left_non >= 2 and right_val >= 2:
                ways = get_comb(left_val, 0) * get_comb(right_val, 2) * get_comb(left_non, 2) * get_comb(right_non, 0)
                ways_k_ge_3 = (ways_k_ge_3 + ways) % MOD
            
            ans = (ans + ways_k_ge_3) % MOD
            
            # Case 2: k = 2 (val appears exactly 2 times in subsequence)
            # We need exactly 1 more val from left+right.
            # The remaining 2 elements must be non-val and distinct from each other.
            
            ways_k_eq_2 = 0
            
            # Option A: 1 val from left, 0 val from right.
            #   Left picks: 1 val, 1 non-val.
            #   Right picks: 0 val, 1 non-val.
            #   Condition: The 2 non-val elements (one from left, one from right) must be distinct.
            
            if left_val >= 1 and right_val >= 0 and left_non >= 1 and right_non >= 1:
                # Ways to pick 1 val from left: C(left_val, 1)
                # Ways to pick 1 non-val from left: left_non
                # Ways to pick 0 val from right: 1
                # Ways to pick 1 non-val from right: right_non
                
                # Total pairs (non_val_left, non_val_right) = left_non * right_non
                # Bad pairs: where non_val_left == non_val_right.
                # For each value u != val, count = left_counts[u] * right_counts[u].
                # Sum these up.
                
                bad_pairs = 0
                for u in left_counts:
                    if u in right_counts:
                        bad_pairs = (bad_pairs + left_counts[u] * right_counts[u]) % MOD
                
                total_pairs = (left_non * right_non) % MOD
                distinct_pairs = (total_pairs - bad_pairs + MOD) % MOD
                
                ways = get_comb(left_val, 1) * distinct_pairs % MOD
                ways_k_eq_2 = (ways_k_eq_2 + ways) % MOD
            
            # Option B: 0 val from left, 1 val from right.
            #   Left picks: 0 val, 2 non-val.
            #   Right picks: 1 val, 0 non-val.
            #   Condition: The 2 non-val elements from left must be distinct.
            
            if left_val >= 0 and right_val >= 1 and left_non >= 2:
                # Calculate distinct pairs from left
                same_pairs_left = 0
                for count in left_counts.values():
                    same_pairs_left = (same_pairs_left + get_comb(count, 2)) % MOD
                
                total_pairs_left = get_comb(left_non, 2)
                distinct_pairs_left = (total_pairs_left - same_pairs_left + MOD) % MOD
                
                # Ways to pick 0 val from left: 1
                # Ways to pick 2 non-val from left: distinct_pairs_left
                # Ways to pick 1 val from right: C(right_val, 1)
                # Ways to pick 0 non-val from right: 1
                
                ways = distinct_pairs_left * get_comb(right_val, 1) % MOD
                ways_k_eq_2 = (ways_k_eq_2 + ways) % MOD
            
            ans = (ans + ways_k_eq_2) % MOD
            
        return ans