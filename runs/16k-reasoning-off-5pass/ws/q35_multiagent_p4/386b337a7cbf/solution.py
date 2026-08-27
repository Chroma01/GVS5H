class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        # dp is a dictionary: key = (current_alternating_sum, next_parity)
        # value = maximum product achievable for that state
        # next_parity: 0 means next element added will be at even index (added to sum)
        #              1 means next element added will be at odd index (subtracted from sum)
        # We only store non-empty subsequences.
        dp = {}
        
        for x in nums:
            # Create a new_dp as a copy of current dp (this represents skipping x)
            new_dp = dp.copy()
            
            # Option 1: Start a new subsequence with x
            # This subsequence has one element at index 0 (even), so sum = x, next_parity = 1
            if x <= limit:
                state = (x, 1)
                if state not in new_dp or new_dp[state] < x:
                    new_dp[state] = x
            
            # Option 2: Extend existing subsequences
            for (s, p), prod in dp.items():
                if p == 0:
                    # Next element is at even index in subsequence, so add x
                    ns = s + x
                    np = 1
                else:
                    # Next element is at odd index in subsequence, so subtract x
                    ns = s - x
                    np = 0
                
                nprod = prod * x
                if nprod <= limit:
                    state = (ns, np)
                    if state not in new_dp or new_dp[state] < nprod:
                        new_dp[state] = nprod
            
            dp = new_dp
        
        # Find the maximum product among all states with alternating sum equal to k
        ans = -1
        for (s, p), prod in dp.items():
            if s == k:
                if prod > ans:
                    ans = prod
        
        return ans