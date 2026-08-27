from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        # Constraints analysis:
        # nums.length <= 150, nums[i] <= 12.
        # Max possible alternating sum magnitude is 150 * 12 = 1800.
        # k can be up to 10^5, but if |k| > 1800, it's impossible.
        # limit <= 5000.
        
        if abs(k) > 1800:
            return -1
        
        OFFSET = 1800
        MAX_SUM = 3601  # Range [-1800, 1800] -> size 3601
        
        # dp[parity][sum] stores the maximum product for a subsequence with:
        # parity 0: next element will be ADDED (even index in subsequence)
        # parity 1: next element will be SUBTRACTED (odd index in subsequence)
        # Initialize with -1 to represent unreachable states.
        dp = [[-1] * MAX_SUM for _ in range(2)]
        
        # possible[parity][sum] is a boolean indicating if the state is reachable by a NON-EMPTY subsequence.
        possible = [[False] * MAX_SUM for _ in range(2)]
        
        # Base case: Empty subsequence
        # Sum = 0, Product = 1, Parity = 0 (next is even index -> add)
        dp[0][OFFSET] = 1
        # possible[0][OFFSET] remains False
        
        for x in nums:
            # Create copies to avoid using the same number multiple times in one step
            new_dp = [row[:] for row in dp]
            new_possible = [row[:] for row in possible]
            
            for p in range(2):
                for s in range(MAX_SUM):
                    if dp[p][s] == -1:
                        continue
                    
                    current_prod = dp[p][s]
                    is_non_empty = possible[p][s]
                    
                    # Try to include x in the subsequence
                    new_p = 1 - p
                    
                    if p == 0:
                        new_s = s + x
                    else:
                        new_s = s - x
                    
                    if 0 <= new_s < MAX_SUM:
                        if current_prod == 0:
                            new_prod = 0
                        else:
                            new_prod = current_prod * x
                            if new_prod > limit:
                                new_prod = limit + 1
                        
                        if new_prod <= limit:
                            if new_dp[new_p][new_s] < new_prod:
                                new_dp[new_p][new_s] = new_prod
                            new_possible[new_p][new_s] = True
            
            dp = new_dp
            possible = new_possible
            
        target_idx = OFFSET + k
        ans = -1
        
        if 0 <= target_idx < MAX_SUM:
            if dp[0][target_idx] != -1 and possible[0][target_idx]:
                ans = max(ans, dp[0][target_idx])
            if dp[1][target_idx] != -1 and possible[1][target_idx]:
                ans = max(ans, dp[1][target_idx])
                
        return ans