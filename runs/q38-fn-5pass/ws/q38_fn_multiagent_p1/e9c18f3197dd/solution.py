from typing import List
from math import gcd

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        if not target:
            return 0
        if not nums:
            return 0

        m = len(target)
        size = 1 << m
        full = size - 1

        max_num = max(nums)

        # Feasible upper bound under the constraints:
        # assign each target element to a distinct nums element and move it
        # to the next multiple of that target, costing at most target[i] - 1.
        upper_bound = sum(t - 1 for t in target)

        # If every target is 1, every existing positive nums element already works.
        if upper_bound == 0:
            return 0

        INF = upper_bound + 1
        cap = max_num + upper_bound

        # lcms[mask] = LCM of targets in mask, capped at cap + 1.
        lcms = [1] * size
        for mask in range(1, size):
            low_bit = mask & -mask
            idx = low_bit.bit_length() - 1
            prev = mask ^ low_bit

            a = lcms[prev]
            if a > cap:
                lcms[mask] = cap + 1
            else:
                b = target[idx]
                g = gcd(a, b)
                l = (a // g) * b
                lcms[mask] = l if l <= cap else cap + 1

        # For each already-covered mask, precompute all nonempty subsets of
        # still-uncovered targets that the current number may newly satisfy.
        transitions = [[] for _ in range(size)]
        for mask in range(size):
            remaining = full ^ mask
            sub = remaining
            while sub:
                transitions[mask].append((mask | sub, sub))
                sub = (sub - 1) & remaining

        # Precompute subset costs for each distinct value in nums.
        cost_by_value = {}
        for x in set(nums):
            # Defensive handling for zero, though constraints have nums[i] >= 1.
            # 0 is a multiple of every positive target.
            if x == 0:
                cost_by_value[x] = [0] * size
                continue

            costs = [0] * size
            for mask in range(1, size):
                l = lcms[mask]
                if l > cap:
                    costs[mask] = INF
                else:
                    r = x % l
                    c = 0 if r == 0 else l - r
                    costs[mask] = c if c <= upper_bound else INF
            cost_by_value[x] = costs

        dp = [INF] * size
        dp[0] = 0

        for x in nums:
            costs = cost_by_value[x]
            new_dp = dp[:]  # option: do not use this number

            for mask, base in enumerate(dp):
                if base == INF:
                    continue

                for new_mask, sub in transitions[mask]:
                    c = costs[sub]
                    if c == INF:
                        continue

                    val = base + c
                    if val < new_dp[new_mask]:
                        new_dp[new_mask] = val

            dp = new_dp

            if dp[full] == 0:
                return 0

        return dp[full]