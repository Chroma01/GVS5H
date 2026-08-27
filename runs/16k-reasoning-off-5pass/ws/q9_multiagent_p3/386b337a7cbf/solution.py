from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        # Dictionary to store max product for state (parity, current_sum)
        # parity: 0 means next element is added (even length subsequence so far)
        # parity: 1 means next element is subtracted (odd length subsequence so far)
        # current_sum: the alternating sum of the subsequence
        
        # Initialize dp with no states. We handle "starting new" explicitly.
        dp = {}
        
        # Temporary dictionary for updates in the current iteration
        next_dp = {}
        
        for x in nums:
            # Option 1: Start a new subsequence with x as the first element.
            # Index 0 is added. So parity becomes 1 (next will be subtracted).
            # Sum becomes x. Product becomes x.
            # Valid only if x <= limit.
            if x <= limit:
                state = (1, x)
                if state not in next_dp or next_dp[state] < x:
                    next_dp[state] = x
            
            # Option 2: Extend existing subsequences
            for (p, s), prod in dp.items():
                # If p == 0, next element is added (+)
                if p == 0:
                    new_sum = s + x
                    new_prod = prod * x
                    new_parity = 1
                    if new_prod <= limit:
                        state = (new_parity, new_sum)
                        if state not in next_dp or next_dp[state] < new_prod:
                            next_dp[state] = new_prod
                # If p == 1, next element is subtracted (-)
                else:
                    new_sum = s - x
                    new_prod = prod * x
                    new_parity = 0
                    if new_prod <= limit:
                        state = (new_parity, new_sum)
                        if state not in next_dp or next_dp[state] < new_prod:
                            next_dp[state] = new_prod
            
            # Merge next_dp into dp, keeping the maximum product for each state
            for state, val in next_dp.items():
                if state not in dp or dp[state] < val:
                    dp[state] = val
            
            # Clear next_dp for the next iteration
            next_dp = {}
        
        # Check for the target alternating sum k
        # The subsequence can end with either parity (0 or 1)
        ans = -1
        target_states = [(0, k), (1, k)]
        
        for p, s in target_states:
            if (p, s) in dp:
                ans = max(ans, dp[(p, s)])
        
        return ans