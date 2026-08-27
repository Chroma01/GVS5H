class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        # Offset for negative sums. Max possible sum magnitude is 150 * 12 = 1800.
        OFFSET = 2000
        MAX_SUM_IDX = 4001  # 0 to 4000
        
        # dp[s][sign] stores the max product for a non-empty subsequence
        # with alternating sum s (shifted by OFFSET) and next sign 'sign'.
        # sign = 1 means next element is added (current length is even)
        # sign = -1 means next element is subtracted (current length is odd)
        # Initialize with -1 to represent invalid/unreachable states.
        dp = [[-1] * 2 for _ in range(MAX_SUM_IDX)]
        
        for x in nums:
            # Create a new DP table for the current iteration to avoid using updated values in the same step
            new_dp = [row[:] for row in dp]
            
            # Option 1: Start a new subsequence with x (from empty subsequence)
            # Empty subsequence has sum 0, next sign is 1.
            # Adding x: new sum = 0 + 1*x = x, new sign = -1 (next will be subtracted)
            ns = OFFSET + x
            np_val = x
            if np_val <= limit and 0 <= ns < MAX_SUM_IDX:
                if np_val > new_dp[ns][-1]:
                    new_dp[ns][-1] = np_val
            
            # Option 2: Extend existing non-empty subsequences
            # We iterate over all possible sums and signs
            for s in range(MAX_SUM_IDX):
                for sign in [1, -1]:
                    prod = dp[s][sign]
                    if prod == -1:
                        continue
                    
                    # Calculate new sum and new product
                    # If sign is 1, we add x; if sign is -1, we subtract x
                    add_val = x if sign == 1 else -x
                    ns = s + add_val
                    np_val = prod * x
                    
                    # Check bounds and limit
                    if 0 <= ns < MAX_SUM_IDX and np_val <= limit:
                        # The next sign flips
                        new_sign = -sign
                        if np_val > new_dp[ns][new_sign]:
                            new_dp[ns][new_sign] = np_val
            
            dp = new_dp
        
        # The target alternating sum is k.
        # We need to check both signs for the state corresponding to k.
        target_idx = OFFSET + k
        ans = -1
        
        if 0 <= target_idx < MAX_SUM_IDX:
            ans = max(ans, dp[target_idx][1], dp[target_idx][-1])
            
        return ans