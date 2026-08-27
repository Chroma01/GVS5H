from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        # Constraints analysis:
        # nums.length <= 150, nums[i] <= 12.
        # Max possible sum = 150 * 12 = 1800.
        # Min possible sum = -150 * 12 = -1800.
        # Range size needed = 3600. We use 4000 for safety.
        OFFSET = 2000
        MAX_SUM = 4000
        
        # dp[s][0]: max product with sum s, next operation is ADD (even index in subsequence)
        # dp[s][1]: max product with sum s, next operation is SUB (odd index in subsequence)
        # Initialize with -1 to represent unreachable states.
        dp = [[-1] * 2 for _ in range(MAX_SUM)]
        
        # exists[s][p]: boolean, True if the state (s, p) is reachable by a non-empty subsequence
        exists = [[False] * 2 for _ in range(MAX_SUM)]
        
        # Base case: Empty subsequence
        # Sum = 0, Next op = ADD (index 0 is even)
        # Product = 1 (identity for multiplication)
        # exists = False (it is empty)
        dp[OFFSET][0] = 1
        exists[OFFSET][0] = False
        
        # Iterate through each number in nums
        for x in nums:
            # Create copies to avoid using updated values from the current step
            new_dp = [row[:] for row in dp]
            new_exists = [row[:] for row in exists]
            
            for s in range(MAX_SUM):
                # If current state is unreachable, skip
                if dp[s][0] == -1 and dp[s][1] == -1:
                    continue
                
                # Try to add x to the subsequence
                
                # Case 1: Current state expects ADD (parity 0)
                # Transition: sum becomes s + x, next becomes SUB (parity 1)
                if dp[s][0] != -1:
                    new_s = s + x
                    if 0 <= new_s < MAX_SUM:
                        new_prod = dp[s][0] * x
                        # Taking x makes the subsequence non-empty
                        new_state_exists = True 
                        
                        if new_prod > new_dp[new_s][1]:
                            new_dp[new_s][1] = new_prod
                            new_exists[new_s][1] = new_state_exists
                        elif new_prod == new_dp[new_s][1]:
                            # If products are equal, prefer non-empty over empty
                            if new_state_exists and not new_exists[new_s][1]:
                                new_exists[new_s][1] = True
                
                # Case 2: Current state expects SUB (parity 1)
                # Transition: sum becomes s - x, next becomes ADD (parity 0)
                if dp[s][1] != -1:
                    new_s = s - x
                    if 0 <= new_s < MAX_SUM:
                        new_prod = dp[s][1] * x
                        new_state_exists = True
                        
                        if new_prod > new_dp[new_s][0]:
                            new_dp[new_s][0] = new_prod
                            new_exists[new_s][0] = new_state_exists
                        elif new_prod == new_dp[new_s][0]:
                            if new_state_exists and not new_exists[new_s][0]:
                                new_exists[new_s][0] = True
            
            dp = new_dp
            exists = new_exists
        
        # Check the target sum k
        target_idx = k + OFFSET
        if 0 <= target_idx < MAX_SUM:
            candidates = []
            for p in range(2):
                # Only consider states reachable by a non-empty subsequence
                if exists[target_idx][p]:
                    prod = dp[target_idx][p]
                    if prod <= limit:
                        candidates.append(prod)
            
            if candidates:
                return max(candidates)
            else:
                return -1
        else:
            return -1