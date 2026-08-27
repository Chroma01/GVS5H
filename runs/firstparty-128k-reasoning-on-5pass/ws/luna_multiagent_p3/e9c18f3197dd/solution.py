from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        # Duplicate targets represent the same requirement, so remove them.
        target = list(dict.fromkeys(target))
        k = len(target)
        size = 1 << k
        full = size - 1

        # Compute the LCM for every nonempty target subset.
        subset_lcm = [1] * size
        for mask in range(1, size):
            bit = mask & -mask
            index = bit.bit_length() - 1
            previous = mask ^ bit
            subset_lcm[mask] = (
                subset_lcm[previous]
                // gcd(subset_lcm[previous], target[index])
                * target[index]
            )

        inf = 10**100
        dp = [inf] * size
        dp[0] = 0

        for value in nums:
            # For each subset, calculate the cost and all targets
            # incidentally covered by the resulting value.
            gains = [None] * size
            for mask in range(1, size):
                lcm_value = subset_lcm[mask]
                increment = (-value) % lcm_value
                new_value = value + increment

                covered = 0
                for i, t in enumerate(target):
                    if new_value % t == 0:
                        covered |= 1 << i

                gains[mask] = (increment, covered)

            # Fresh-layer transitions: either skip this number or use it once.
            next_dp = dp[:]

            for state in range(size):
                base = dp[state]
                if base == inf:
                    continue

                missing = full ^ state
                subset = missing

                while subset:
                    increment, covered = gains[subset]
                    new_state = state | covered
                    candidate = base + increment

                    if candidate < next_dp[new_state]:
                        next_dp[new_state] = candidate

                    subset = (subset - 1) & missing

            dp = next_dp

        return dp[full]