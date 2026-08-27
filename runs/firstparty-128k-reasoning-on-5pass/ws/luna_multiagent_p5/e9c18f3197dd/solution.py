from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        state_count = 1 << m
        full_mask = state_count - 1

        # lcms[mask] is the LCM of all target values represented by mask.
        lcms = [1] * state_count
        for mask in range(1, state_count):
            previous = mask & (mask - 1)
            added_bit = mask ^ previous
            index = added_bit.bit_length() - 1
            lcms[mask] = (
                lcms[previous] // gcd(lcms[previous], target[index])
                * target[index]
            )

        inf = 10**30
        dp = [inf] * state_count
        dp[0] = 0

        for value in nums:
            # Cost of incrementing this value to a multiple of each subset LCM.
            costs = [0] * state_count
            for subset in range(1, state_count):
                costs[subset] = (-value) % lcms[subset]

            # Skipping the current value is allowed.
            next_dp = dp[:]

            for covered_mask, current_cost in enumerate(dp):
                if current_cost == inf:
                    continue

                for subset in range(1, state_count):
                    new_mask = covered_mask | subset
                    candidate = current_cost + costs[subset]
                    if candidate < next_dp[new_mask]:
                        next_dp[new_mask] = candidate

            dp = next_dp

        return dp[full_mask]