from typing import List

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
            
        # dp[i] stores the minimum cost to partition nums[0...i-1] (prefix of length i)
        # cnt[i] stores the minimum number of subarrays to achieve dp[i]
        # We use a large number for infinity
        INF = float('inf')
        dp = [INF] * (n + 1)
        cnt = [INF] * (n + 1)
        
        # Base case: 0 elements cost 0 and have 0 subarrays
        dp[0] = 0
        cnt[0] = 0
        
        # Iterate through all end points of the prefix
        for i in range(1, n + 1):
            # Try all possible start points j for the last subarray
            # The last subarray is nums[j-1 ... i-1] (0-indexed in original array)
            # In terms of prefix sums, it corresponds to range [j, i)
            for j in range(1, i + 1):
                # Sum of cost in the last subarray (only subarray sum matters here)
                sum_cost = P_cost[i] - P_cost[j-1]
                
                # Number of subarrays in the prefix before this one
                prev_cnt = cnt[j-1]
                
                # If the prefix [0...j-1] is unreachable, skip
                if dp[j-1] == INF:
                    continue
                
                # The current subarray is the (prev_cnt + 1)-th subarray
                # According to the problem statement:
                # Cost = (Sum(nums[0]...nums[r]) + k * order) * Sum(cost[l]...cost[r])
                # Here r corresponds to i-1 (0-indexed), so Sum(nums[0]...nums[r]) is P_nums[i]
                # Sum(cost[l]...cost[r]) is sum_cost
                current_sub_cost = (P_nums[i] + k * (prev_cnt + 1)) * sum_cost
                
                total_cost = dp[j-1] + current_sub_cost
                new_cnt = prev_cnt + 1
                
                # Update dp[i] and cnt[i]
                if total_cost < dp[i]:
                    dp[i] = total_cost
                    cnt[i] = new_cnt
                elif total_cost == dp[i]:
                    # Tie-breaking: choose the partition with fewer subarrays
                    # This is crucial because fewer subarrays mean a smaller multiplier 
                    # for future subarrays (since cost depends on k * order).
                    if new_cnt < cnt[i]:
                        cnt[i] = new_cnt
                        
        return dp[n]