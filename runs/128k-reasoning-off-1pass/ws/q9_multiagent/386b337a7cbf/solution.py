from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        # Constraints analysis:
        # nums.length <= 150
        # 0 <= nums[i] <= 12
        # Max possible alternating sum magnitude = 150 * 12 = 1800
        # We need an offset to handle negative sums in array indexing.
        OFFSET = 1800
        MAX_SUM_RANGE = 3601  # Covers -1800 to 1800
        
        # dp[s][p] stores the maximum product for alternating sum s (offset by OFFSET)
        # and parity p (0 for even length, 1 for odd length).
        # Initialize with -1 to represent unreachable states.
        dp = [[-1] * 2 for _ in range(MAX_SUM_RANGE)]
        
        # Iterate through each number in nums
        for x in nums:
            # We collect updates to avoid using the same element multiple times in one step
            # (standard 0/1 knapsack optimization)
            new_updates = {} 
            
            # 1. Start a new subsequence with just the current number x
            # Length = 1 (Odd parity), Sum = x, Product = x
            if x <= limit:
                new_sum_idx = x + OFFSET
                if 0 <= new_sum_idx < MAX_SUM_RANGE:
                    key = (new_sum_idx, 1)
                    new_updates[key] = x
            
            # 2. Extend existing subsequences
            for s_idx in range(MAX_SUM_RANGE):
                current_sum = s_idx - OFFSET
                for parity in range(2):
                    current_prod = dp[s_idx][parity]
                    
                    if current_prod == -1:
                        continue
                    
                    # Calculate new state based on current parity
                    if parity == 0:
                        # Current length is Even. Appending x makes it Odd.
                        # In alternating sum definition: x_0 - x_1 + x_2 ...
                        # If current subsequence is [a, b] (len 2, even), sum = a - b.
                        # Appending x makes it [a, b, x]. x is at index 2 (even).
                        # New sum = (a - b) + x = current_sum + x.
                        new_sum = current_sum + x
                        new_prod = current_prod * x
                    else:
                        # Current length is Odd. Appending x makes it Even.
                        # If current subsequence is [a] (len 1, odd), sum = a.
                        # Appending x makes it [a, x]. x is at index 1 (odd).
                        # New sum = a - x = current_sum - x.
                        new_sum = current_sum - x
                        new_prod = current_prod * x
                    
                    # Check constraints
                    if new_prod <= limit:
                        new_sum_idx = new_sum + OFFSET
                        if 0 <= new_sum_idx < MAX_SUM_RANGE:
                            key = (new_sum_idx, 1 - parity) # Flip parity
                            if key not in new_updates or new_updates[key] < new_prod:
                                new_updates[key] = new_prod
            
            # Apply updates to the DP table
            for (s_idx, p), prod in new_updates.items():
                if prod > dp[s_idx][p]:
                    dp[s_idx][p] = prod
        
        # After processing all numbers, look for the answer
        target_idx = k + OFFSET
        if 0 <= target_idx < MAX_SUM_RANGE:
            ans = -1
            # Check both parities (even length and odd length)
            for p in range(2):
                if dp[target_idx][p] != -1:
                    ans = max(ans, dp[target_idx][p])
            
            return ans
        
        return -1