from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        # Constraints analysis:
        # nums.length <= 150
        # 0 <= nums[i] <= 12
        # -10^5 <= k <= 10^5
        # 1 <= limit <= 5000
        
        # The maximum possible alternating sum magnitude is 150 * 12 = 1800.
        # We need an offset to handle negative indices in the DP array.
        OFFSET = 1800
        MAX_SUM = 3601  # Range from -1800 to 1800
        
        # dp_empty tracks states reachable from the empty subsequence (only initially)
        # dp_non_empty tracks states reachable from at least one picked element
        
        # Initialize DP tables with -1 (representing unreachable states)
        dp_empty = [[-1] * 2 for _ in range(MAX_SUM)]
        dp_non_empty = [[-1] * 2 for _ in range(MAX_SUM)]
        
        # Base case: Empty subsequence has sum 0, next parity is 0 (even), product 1
        dp_empty[OFFSET][0] = 1
        
        # Iterate through each number in nums
        for x in nums:
            # Create new DP tables for the current step to avoid using the same item multiple times in one step
            new_dp_empty = [row[:] for row in dp_empty]
            new_dp_non_empty = [row[:] for row in dp_non_empty]
            
            # 1. Transitions from dp_empty (picking the first element)
            # If we pick x, we move from empty to non-empty
            # Current state: sum=0, parity=0, prod=1
            # New state: sum = 0 + x, parity = 1, prod = 1 * x
            if x <= limit:
                new_sum = OFFSET + x
                if 0 <= new_sum < MAX_SUM:
                    new_prod = 1 * x
                    if new_prod <= limit:
                        new_dp_non_empty[new_sum][1] = max(new_dp_non_empty[new_sum][1], new_prod)
            
            # 2. Transitions from dp_non_empty (picking subsequent elements)
            # We iterate over all reachable states in dp_non_empty
            for s in range(MAX_SUM):
                for p in range(2):
                    if dp_non_empty[s][p] == -1:
                        continue
                    
                    current_prod = dp_non_empty[s][p]
                    
                    # Option A: Pick x
                    # If p == 0 (next is even index), add x. New parity becomes 1.
                    # If p == 1 (next is odd index), subtract x. New parity becomes 0.
                    
                    if p == 0:
                        new_s = s + x
                        new_p = 1
                    else:
                        new_s = s - x
                        new_p = 0
                    
                    # Check bounds for new_s
                    if 0 <= new_s < MAX_SUM:
                        new_prod = current_prod * x
                        if new_prod <= limit:
                            new_dp_non_empty[new_s][new_p] = max(new_dp_non_empty[new_s][new_p], new_prod)
            
            # Update DP tables
            dp_empty = new_dp_empty
            dp_non_empty = new_dp_non_empty
            
        # The answer must come from dp_non_empty
        # We look for sum == k (index = k + OFFSET)
        target_idx = k + OFFSET
        if 0 <= target_idx < MAX_SUM:
            ans0 = dp_non_empty[target_idx][0]
            ans1 = dp_non_empty[target_idx][1]
            
            result = max(ans0, ans1)
            return result if result != -1 else -1
        else:
            return -1