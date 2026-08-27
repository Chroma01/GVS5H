from typing import List
from collections import Counter

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # Precompute prefix counts
        # prefix_counts[i] contains counts of all numbers in nums[0...i-1]
        prefix_counts = [{} for _ in range(n + 1)]
        for i in range(n):
            prefix_counts[i+1] = prefix_counts[i].copy()
            prefix_counts[i+1][nums[i]] = prefix_counts[i+1].get(nums[i], 0) + 1
            
        # Precompute suffix counts
        # suffix_counts[i] contains counts of all numbers in nums[i...n-1]
        suffix_counts = [{} for _ in range(n + 1)]
        for i in range(n - 1, -1, -1):
            suffix_counts[i] = suffix_counts[i+1].copy()
            suffix_counts[i][nums[i]] = suffix_counts[i].get(nums[i], 0) + 1
            
        def get_combinations(n, k):
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

        def calc_e3(weights):
            # Calculate sum of products of 3 distinct weights using DP
            # dp[k] stores the sum of products of k distinct elements processed so far
            dp = [0] * 4
            dp[0] = 1
            for w in weights:
                for k in range(3, 0, -1):
                    dp[k] = (dp[k] + dp[k-1] * w) % MOD
            return dp[3]

        total_ways = 0
        
        # Iterate through each element as the potential middle element of the subsequence
        # The middle element is at index 'idx' in the original array.
        # We need at least 2 elements before 'idx' and 2 elements after 'idx'.
        # So idx ranges from 2 to n - 3.
        for idx in range(2, n - 2):
            x = nums[idx]
            
            # Counts of x in left (0 to idx-1) and right (idx+1 to n-1) parts
            cnt_left_x = prefix_counts[idx].get(x, 0)
            cnt_right_x = suffix_counts[idx+1].get(x, 0)
            
            # Total available slots on left and right
            total_left = idx
            total_right = n - 1 - idx
            
            # Non-x counts available
            non_x_left = total_left - cnt_left_x
            non_x_right = total_right - cnt_right_x
            
            # Iterate over possible number of x's chosen from left (l) and right (r)
            # We need to choose exactly 2 from left and 2 from right in total (excluding the middle x)
            # So l + r must be between 1 and 4.
            # l can be 0, 1, 2 (bounded by cnt_left_x and 2)
            # r can be 0, 1, 2 (bounded by cnt_right_x and 2)
            for l in range(0, 3):
                for r in range(0, 3):
                    if l + r == 0:
                        continue # x count = 1, not a mode
                    
                    K = 1 + l + r # Total count of x in the subsequence
                    rem = 4 - (l + r) # Number of non-x elements to pick
                    
                    ways_non_x = 0
                    
                    if rem == 0:
                        # Case K=5: x appears 4 times (middle + 3 others). 
                        # No non-x elements needed.
                        ways_non_x = 1
                    elif rem == 1:
                        # Case K=4: x appears 3 times. 
                        # Pick 1 non-x element. Any non-x element is valid (freq 1 < 3).
                        ways_non_x = non_x_left + non_x_right
                    elif rem == 2:
                        # Case K=3: x appears 2 times.
                        # Pick 2 non-x elements. Max freq of non-x is 2, which is < 3.
                        # So any 2 non-x elements (same or different values) are valid.
                        # Ways = C(left, 2) + C(right, 2) + left * right
                        ways_non_x = (get_combinations(non_x_left, 2) + 
                                     get_combinations(non_x_right, 2) + 
                                     non_x_left * non_x_right)
                    elif rem == 3:
                        # Case K=2: x appears 1 time (middle) + 1 other x.
                        # Pick 3 non-x elements. Max freq of non-x must be < 2, so must be 1.
                        # Thus, all 3 non-x elements must be distinct values.
                        # We need to choose 3 distinct values from the union of non-x values on left and right.
                        # For each value v, let W_v = count(v, left) + count(v, right).
                        # We need sum of products of 3 distinct W_v's.
                        
                        val_counts = {}
                        # Aggregate counts from left
                        for v, c in prefix_counts[idx].items():
                            if v == x: continue
                            val_counts[v] = val_counts.get(v, 0) + c
                        # Aggregate counts from right
                        for v, c in suffix_counts[idx+1].items():
                            if v == x: continue
                            val_counts[v] = val_counts.get(v, 0) + c
                        
                        w_list = list(val_counts.values())
                        ways_non_x = calc_e3(w_list)
                    else:
                        ways_non_x = 0
                    
                    # Ways to choose l copies of x from left and r copies of x from right
                    ways_x = get_combinations(cnt_left_x, l) * get_combinations(cnt_right_x, r)
                    
                    total_ways = (total_ways + ways_x * ways_non_x) % MOD
                    
        return total_ways