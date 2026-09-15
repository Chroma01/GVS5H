from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0

        prefix_nums = [0] * (n + 1)
        prefix_cost = [0] * (n + 1)

        for i in range(n):
            prefix_nums[i + 1] = prefix_nums[i] + nums[i]
            prefix_cost[i + 1] = prefix_cost[i] + cost[i]

        total_cost = prefix_cost[n]
        INF = 10**30

        # dp[r] is the minimum transformed path cost to reach prefix length r.
        # It is not the original cost for prefix r alone; it is exact for paths
        # that will be extended to the full array.
        dp = [INF] * (n + 1)
        dp[0] = 0

        pn = prefix_nums
        pc = prefix_cost

        for r in range(1, n + 1):
            query = pn[r] + k
            best = INF

            for p in range(r):
                candidate = dp[p] - query * pc[p]
                if candidate < best:
                    best = candidate

            dp[r] = pn[r] * pc[r] + k * total_cost + best

        return dp[n]