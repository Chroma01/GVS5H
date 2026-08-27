from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1

        # LCM for every subset of target indices.
        subset_lcm = [1] * (1 << m)
        for mask in range(1, 1 << m):
            bit = mask & -mask
            idx = bit.bit_length() - 1
            prev = mask ^ bit
            subset_lcm[mask] = (
                subset_lcm[prev] // gcd(subset_lcm[prev], target[idx])
                * target[idx]
            )

        inf = 10**30
        dp = [inf] * (1 << m)
        dp[0] = 0

        for value in nums:
            # Skipping this value is always allowed.
            next_dp = dp[:]

            # Only assign targets not already covered. Assigning an already
            # covered target cannot improve the cost.
            for covered in range(1 << m):
                if dp[covered] == inf:
                    continue

                remaining = full ^ covered
                subset = remaining

                while subset:
                    multiple = subset_lcm[subset]
                    remainder = value % multiple
                    cost = 0 if remainder == 0 else multiple - remainder
                    new_mask = covered | subset
                    candidate = dp[covered] + cost

                    if candidate < next_dp[new_mask]:
                        next_dp[new_mask] = candidate

                    subset = (subset - 1) & remaining

            dp = next_dp
            if dp[full] == 0:
                return 0

        return dp[full]