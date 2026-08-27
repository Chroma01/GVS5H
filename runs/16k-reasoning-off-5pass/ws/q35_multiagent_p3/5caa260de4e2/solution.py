class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        
        # Precompute prefix sums for nums and cost
        # P_nums[i] = sum(nums[0]...nums[i-1])
        # P_cost[i] = sum(cost[0]...cost[i-1])
        P_nums = [0] * (n + 1)
        P_cost = [0] * (n + 1)
        for i in range(n):
            P_nums[i+1] = P_nums[i] + nums[i]
            P_cost[i+1] = P_cost[i] + cost[i]
            
        # dp[i][j] = min cost to partition first i elements into j subarrays
        # i ranges from 0 to n
        # j ranges from 0 to n
        # Initialize with infinity
        INF = float('inf')
        dp = [[INF] * (n + 1) for _ in range(n + 1)]
        dp[0][0] = 0
        
        # Iterate over number of subarrays j from 1 to n
        for j in range(1, n + 1):
            # Iterate over end position i from j to n (need at least j elements for j subarrays)
            for i in range(j, n + 1):
                # The j-th subarray is nums[l...i-1] for some l in [j-1, i-1]
                # l is the start index of the last subarray, so the previous j-1 subarrays cover nums[0...l-1]
                # We need dp[l][j-1] to be valid, so l >= j-1
                # Also, the last subarray must have at least 1 element, so l < i
                
                # To optimize, we can iterate l from j-1 to i-1
                # The cost of the j-th subarray nums[l...i-1] is:
                # (P_nums[i] - P_nums[l] + k * j) * (P_cost[i] - P_cost[l])
                
                # Let's compute this efficiently
                # We'll iterate l and update dp[i][j]
                
                # Precompute terms that depend on i and j for the current state
                # term1 = P_nums[i] + k * j
                # term2 = P_cost[i]
                # Then for each l:
                #   subarray_nums_sum = P_nums[i] - P_nums[l]
                #   subarray_cost_sum = P_cost[i] - P_cost[l]
                #   cost = (subarray_nums_sum + k * j) * subarray_cost_sum
                #        = (term1 - P_nums[l]) * (term2 - P_cost[l])
                
                term1 = P_nums[i] + k * j
                term2 = P_cost[i]
                
                best_prev = INF
                for l in range(j - 1, i):
                    if dp[l][j-1] == INF:
                        continue
                    # Calculate cost of subarray from l to i-1 (0-indexed in nums, so indices l to i-1)
                    # sum_nums = P_nums[i] - P_nums[l]
                    # sum_cost = P_cost[i] - P_cost[l]
                    # cost = (sum_nums + k * j) * sum_cost
                    
                    # Using expanded form:
                    # cost = (term1 - P_nums[l]) * (term2 - P_cost[l])
                    sub_cost = (term1 - P_nums[l]) * (term2 - P_cost[l])
                    total = dp[l][j-1] + sub_cost
                    if total < best_prev:
                        best_prev = total
                
                dp[i][j] = best_prev
                
        # The answer is the minimum cost to partition all n elements into any number of subarrays j from 1 to n
        ans = min(dp[n][j] for j in range(1, n + 1))
        return ans