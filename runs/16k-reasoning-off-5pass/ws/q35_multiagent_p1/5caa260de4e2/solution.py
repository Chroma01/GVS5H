class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # Prefix sums for nums and cost
        P_nums = [0] * (n + 1)
        P_cost = [0] * (n + 1)
        for i in range(n):
            P_nums[i+1] = P_nums[i] + nums[i]
            P_cost[i+1] = P_cost[i] + cost[i]
            
        # dp[i][j] = min cost to partition first i elements into exactly j subarrays
        INF = float('inf')
        dp = [[INF] * (n + 1) for _ in range(n + 1)]
        dp[0][0] = 0
        
        for i in range(1, n + 1):
            for j in range(1, i + 1):
                # The last subarray is nums[kk...i-1] (0-indexed)
                # It is the j-th subarray in the partition
                # kk is the number of elements in the prefix before this subarray
                # kk must be at least j-1 (to have j-1 subarrays before)
                # and at most i-1 (at least one element in current subarray)
                for kk in range(j-1, i):
                    if dp[kk][j-1] == INF:
                        continue
                    sum_n = P_nums[i] - P_nums[kk]
                    sum_c = P_cost[i] - P_cost[kk]
                    # Cost of the j-th subarray
                    sub_cost = (sum_n + k * j) * sum_c
                    new_val = dp[kk][j-1] + sub_cost
                    if new_val < dp[i][j]:
                        dp[i][j] = new_val
                        
        return min(dp[n][1:])