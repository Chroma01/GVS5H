from typing import List
from math import gcd
from bisect import bisect_right


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        nums.sort()
        max_num = nums[-1]
        k = len(target)
        full = (1 << k) - 1
        INF = float('inf')

        # cost[mask]: minimum increments to make some single nums element
        # a common multiple of all target values in mask.
        cost = [INF] * (1 << k)

        for mask in range(1, 1 << k):
            # Compute LCM of the subset, capping to avoid huge numbers.
            l = 1
            for i in range(k):
                if mask >> i & 1:
                    t = target[i]
                    l = l // gcd(l, t) * t
                    if l > 10**16:  # safety cap, far beyond any useful value
                        break

            if l > max_num:
                # Every nums element is < l, so the cheapest is raising the
                # largest element up to l itself.
                cost[mask] = l - max_num
            else:
                best = INF
                # For each multiple m of l up to max_num, the best element to
                # raise is the largest nums[j] <= m (cost m - nums[j]).
                for m in range(l, max_num + 1, l):
                    idx = bisect_right(nums, m) - 1
                    if idx >= 0:
                        c = m - nums[idx]
                        if c < best:
                            best = c
                            if best == 0:
                                break
                cost[mask] = best

        # dp[mask]: minimum total increments to cover all targets in mask,
        # partitioning mask into groups each served by one nums element.
        dp = [INF] * (1 << k)
        dp[0] = 0
        for mask in range(1, 1 << k):
            sub = mask
            while sub:
                if dp[mask ^ sub] + cost[sub] < dp[mask]:
                    dp[mask] = dp[mask ^ sub] + cost[sub]
                sub = (sub - 1) & mask

        return dp[full]