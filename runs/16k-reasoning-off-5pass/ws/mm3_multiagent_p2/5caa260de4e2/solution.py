from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # Prefix sums: S[i] = sum of nums[0..i-1], C[i] = sum of cost[0..i-1]
        S = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            S[i+1] = S[i] + nums[i]
            C[i+1] = C[i] + cost[i]
        
        # dp[i] = minimum cost to partition nums[0..i-1]
        # cnt[i] = number of groups in that optimal partition
        dp = [float('inf')] * (n + 1)
        cnt = [0] * (n + 1)
        dp[0] = 0  # empty prefix has cost 0 and 0 groups
        
        for i in range(1, n + 1):
            # Try all possible previous cut positions j
            for j in range(i):
                # Number of groups in prefix [0, j) is cnt[j]
                # The new group [j, i) becomes the (cnt[j] + 1)-th group
                group_num = cnt[j] + 1
                # Sum of nums in [j, i)
                sum_nums = S[i] - S[j]
                # Sum of cost in [j, i)
                sum_cost = C[i] - C[j]
                # Cost of this new group
                group_cost = (sum_nums + k * group_num) * sum_cost
                total_cost = dp[j] + group_cost
                if total_cost < dp[i]:
                    dp[i] = total_cost
                    cnt[i] = group_num
        
        return dp[n]