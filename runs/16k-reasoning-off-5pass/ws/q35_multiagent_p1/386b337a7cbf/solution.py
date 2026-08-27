class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        max_sum = 150 * 12
        offset = max_sum
        # dp[s][p] stores the max product for alternating sum (s - offset) and next parity p
        # p=0: next element will be at even index (positive contribution)
        # p=1: next element will be at odd index (negative contribution)
        dp = [[-1] * 2 for _ in range(2 * max_sum + 1)]
        
        for x in nums:
            # Create a copy of current dp state to avoid using the same element multiple times in one step
            new_dp = [row[:] for row in dp]
            
            # Option 1: Start a new subsequence with x
            if x <= limit:
                s_new = x + offset
                if 0 <= s_new < len(dp):
                    # Next parity is 1 (odd index)
                    if x > new_dp[s_new][1]:
                        new_dp[s_new][1] = x
            
            # Option 2: Extend existing subsequences with x
            for s in range(len(dp)):
                for p in range(2):
                    prod = dp[s][p]
                    if prod == -1:
                        continue
                    
                    # Calculate new sum and parity
                    if p == 0:
                        s_new = s + x
                    else:
                        s_new = s - x
                    
                    p_new = 1 - p
                    prod_new = prod * x
                    
                    if 0 <= s_new < len(dp) and prod_new <= limit:
                        if prod_new > new_dp[s_new][p_new]:
                            new_dp[s_new][p_new] = prod_new
            
            dp = new_dp
        
        # The answer is the max product for alternating sum k, regardless of the next parity
        idx = k + offset
        if 0 <= idx < len(dp):
            ans = max(dp[idx][0], dp[idx][1])
            return ans if ans != -1 else -1
        else:
            return -1