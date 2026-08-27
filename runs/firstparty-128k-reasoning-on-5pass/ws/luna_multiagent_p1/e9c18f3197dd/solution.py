from math import gcd
from typing import List


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        total_masks = 1 << m
        full_mask = total_masks - 1

        # lcms[mask] is the least common multiple of target values in mask.
        lcms = [1] * total_masks
        for mask in range(1, total_masks):
            bit = mask & -mask
            index = bit.bit_length() - 1
            previous = mask ^ bit
            value = target[index]
            lcms[mask] = lcms[previous] // gcd(lcms[previous], value) * value

        inf = 10**30
        dp = [inf] * total_masks
        dp[0] = 0

        for number in nums:
            costs = [0] * total_masks
            for mask in range(1, total_masks):
                remainder = number % lcms[mask]
                costs[mask] = (lcms[mask] - remainder) % lcms[mask]

            # The current number may be unused, or assigned to one subset
            # of targets not already covered.
            next_dp = dp[:]
            for covered, current_cost in enumerate(dp):
                if current_cost == inf:
                    continue

                available = full_mask ^ covered
                subset = available
                while subset:
                    new_mask = covered | subset
                    candidate = current_cost + costs[subset]
                    if candidate < next_dp[new_mask]:
                        next_dp[new_mask] = candidate
                    subset = (subset - 1) & available

            dp = next_dp

        return dp[full_mask]