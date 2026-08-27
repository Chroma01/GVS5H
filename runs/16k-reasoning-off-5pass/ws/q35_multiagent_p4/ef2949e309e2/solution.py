from typing import List
from collections import Counter

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # Precompute suffix frequency map
        suffix_freq = Counter(nums)
        # Initialize sum of squares for suffix
        sum_sq_right = sum(count**2 for count in suffix_freq.values())
        
        prefix_freq = Counter()
        sum_sq_left = 0
        
        total_ways = 0
        
        # Helper for combinations
        def comb(n, k):
            if k < 0 or k > n:
                return 0
            if k == 0 or k == n:
                return 1
            if k > n // 2:
                k = n - k
            res = 1
            for i in range(k):
                res = res * (n - i) // (i + 1)
            return res
        
        for i in range(n):
            v = nums[i]
            
            # Remove current element from suffix
            old_count_suffix = suffix_freq[v]
            new_count_suffix = old_count_suffix - 1
            suffix_freq[v] = new_count_suffix
            if new_count_suffix == 0:
                del suffix_freq[v]
            # Update sum_sq_right
            sum_sq_right = sum_sq_right - old_count_suffix**2 + new_count_suffix**2
            
            c_v_left = prefix_freq.get(v, 0)
            c_v_right = new_count_suffix  # suffix_freq.get(v, 0)
            
            total_left = i
            total_right = n - 1 - i
            
            total_left_non_v = total_left - c_v_left
            total_right_non_v = total_right - c_v_right
            
            sum_sq_left_non_v = sum_sq_left - c_v_left**2
            sum_sq_right_non_v = sum_sq_right - c_v_right**2
            
            ways = 0
            
            # Case 1: v appears 5 times (k_left=2, k_right=2)
            if c_v_left >= 2 and c_v_right >= 2:
                ways += comb(c_v_left, 2) * comb(c_v_right, 2)
            
            # Case 2: v appears 4 times
            # Subcase: k_left=2, k_right=1
            if c_v_left >= 2 and c_v_right >= 1:
                ways += comb(c_v_left, 2) * c_v_right
            # Subcase: k_left=1, k_right=2
            if c_v_left >= 1 and c_v_right >= 2:
                ways += c_v_left * comb(c_v_right, 2)
            
            # Case 3: v appears 3 times
            # Subcase 3a: k_left=2, k_right=0 (choose 2 non-v from right)
            if c_v_left >= 2 and total_right_non_v >= 2:
                left_ways = comb(c_v_left, 2)
                # Number of ways to choose 2 distinct elements from right non-v
                right_ways = (total_right_non_v**2 - sum_sq_right_non_v) // 2
                ways += left_ways * right_ways
            
            # Subcase 3b: k_left=0, k_right=2 (choose 2 non-v from left)
            if total_left_non_v >= 2 and c_v_right >= 2:
                left_ways = (total_left_non_v**2 - sum_sq_left_non_v) // 2
                right_ways = comb(c_v_right, 2)
                ways += left_ways * right_ways
            
            # Subcase 3c: k_left=1, k_right=1 (choose 1 non-v from left, 1 from right, must be distinct)
            if c_v_left >= 1 and c_v_right >= 1 and total_left_non_v >= 1 and total_right_non_v >= 1:
                # Total ways to choose 1 non-v from left and 1 from right without restriction
                total_non_v_pairs = total_left_non_v * total_right_non_v
                # Subtract overlap where the chosen non-v elements are the same value
                overlap = 0
                for x in prefix_freq:
                    if x == v:
                        continue
                    if x in suffix_freq:
                        overlap += prefix_freq[x] * suffix_freq[x]
                
                distinct_non_v_pairs = total_non_v_pairs - overlap
                left_ways = c_v_left  # comb(c_v_left, 1)
                right_ways = c_v_right  # comb(c_v_right, 1)
                ways += left_ways * right_ways * distinct_non_v_pairs
            
            total_ways = (total_ways + ways) % MOD
            
            # Add current element to prefix
            old_count_prefix = prefix_freq.get(v, 0)
            new_count_prefix = old_count_prefix + 1
            sum_sq_left = sum_sq_left - old_count_prefix**2 + new_count_prefix**2
            prefix_freq[v] = new_count_prefix
            
        return total_ways % MOD