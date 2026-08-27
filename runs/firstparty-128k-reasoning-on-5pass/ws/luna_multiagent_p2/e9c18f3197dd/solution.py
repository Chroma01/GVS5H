from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        total_masks = 1 << m

        lcms = [1] * total_masks
        for mask in range(1, total_masks):
            bit = mask & -mask
            index = bit.bit_length() - 1
            previous = mask ^ bit
            lcms[mask] = (
                lcms[previous]
                // gcd(lcms[previous], target[index])
                * target[index]
            )

        inf = 10**30
        dp = [inf] * total_masks
        dp[0] = 0

        for value in nums:
            costs = [0] * total_masks
            for subset in range(1, total_masks):
                costs[subset] = (-value) % lcms[subset]

            next_dp = dp[:]
            for covered in range(total_masks):
                if dp[covered] == inf:
                    continue

                for subset in range(1, total_masks):
                    new_mask = covered | subset
                    candidate = dp[covered] + costs[subset]
                    if candidate < next_dp[new_mask]:
                        next_dp[new_mask] = candidate

            dp = next_dp

        return dp[-1]