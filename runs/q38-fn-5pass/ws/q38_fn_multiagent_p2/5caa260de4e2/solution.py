from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0

        # prefix_num[r] = nums[0] + ... + nums[r-1]
        # prefix_cost[r] = cost[0] + ... + cost[r-1]
        prefix_num = [0] * (n + 1)
        prefix_cost = [0] * (n + 1)

        for i in range(n):
            prefix_num[i + 1] = prefix_num[i] + nums[i]
            prefix_cost[i + 1] = prefix_cost[i] + cost[i]

        total_cost = prefix_cost[n]

        # dp[r] = minimum transformed cost to partition nums[0:r].
        # A cut at position p is not penalized until the next segment is added.
        dp = [0] * (n + 1)

        for r in range(1, n + 1):
            x = prefix_num[r] + k
            cr = prefix_cost[r]

            # First segment: previous cut is at position 0, so no cut penalty.
            best = x * cr

            # Last segment is nums[p:r], where p is a previous cut position.
            for p in range(1, r):
                cp = prefix_cost[p]
                candidate = dp[p] + x * (cr - cp) + k * (total_cost - cp)
                if candidate < best:
                    best = candidate

            dp[r] = best

        return dp[n]