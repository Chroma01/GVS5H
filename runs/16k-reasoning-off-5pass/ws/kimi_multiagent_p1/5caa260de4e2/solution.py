from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        # Prefix sums: preNums[i] = sum(nums[0..i-1]), preCost[i] = sum(cost[0..i-1])
        pre_nums = [0] * (n + 1)
        pre_cost = [0] * (n + 1)
        for i in range(n):
            pre_nums[i + 1] = pre_nums[i] + nums[i]
            pre_cost[i + 1] = pre_cost[i] + cost[i]

        total_cost = pre_cost[n]
        INF = float('inf')

        # dp[r] = minimum total cost to partition nums[0..r-1] completely
        dp = [INF] * (n + 1)
        dp[0] = 0

        for r in range(1, n + 1):
            best = INF
            pr_n = pre_nums[r]
            pr_c = pre_cost[r]
            # Last segment is nums[j..r-1]. Its non-k part is
            # preNums[r] * (preCost[r] - preCost[j]).
            # The sum of k*i*segCost_i over all segments equals
            # k * sum over segments of suffixCost[segment_start],
            # so this segment contributes k * (totalCost - preCost[j]).
            for j in range(r):
                cand = dp[j] + pr_n * (pr_c - pre_cost[j]) + k * (total_cost - pre_cost[j])
                if cand < best:
                    best = cand
            dp[r] = best

        return dp[n]