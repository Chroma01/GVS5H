class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        # dp is a dictionary: key = (current_alternating_sum, next_parity), value = max_product
        # next_parity: 0 means next element will be added (even index in subsequence), 1 means subtracted (odd index)
        dp = {}
        
        for x in nums:
            # Create a copy of current dp states to allow skipping the current number
            new_dp = dp.copy()
            
            # For each existing subsequence state, try appending x
            for (s, p), prod in dp.items():
                if p == 0:
                    new_s = s + x
                else:
                    new_s = s - x
                
                new_p = 1 - p
                new_prod = prod * x
                
                if new_prod <= limit:
                    # Update the new_dp with the new state if it's better
                    key = (new_s, new_p)
                    if key not in new_dp or new_prod > new_dp[key]:
                        new_dp[key] = new_prod
            
            # Start a new subsequence with just x
            # This corresponds to adding x to an empty subsequence (sum=0, next_parity=0)
            new_s = x  # 0 + x since next_parity for empty is 0 (add)
            new_p = 1  # next element after this would be at odd index (subtract)
            new_prod = x
            
            if new_prod <= limit:
                key = (new_s, new_p)
                if key not in new_dp or new_prod > new_dp[key]:
                    new_dp[key] = new_prod
            
            dp = new_dp
        
        # Check for the target alternating sum k
        # The parity at the end doesn't matter for the sum value, but we need to check both
        ans = -1
        for p in [0, 1]:
            if (k, p) in dp:
                if dp[(k, p)] > ans:
                    ans = dp[(k, p)]
        
        return ans