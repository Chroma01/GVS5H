from typing import List
from math import gcd

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        if m == 0:
            return 0

        size = 1 << m
        full = size - 1

        # lcm[mask] = least common multiple of target values whose bits are in mask
        lcm = [1] * size
        for mask in range(1, size):
            lsb = mask & -mask
            i = lsb.bit_length() - 1
            prev = mask ^ lsb
            a = lcm[prev]
            b = target[i]
            lcm[mask] = a // gcd(a, b) * b

        # For each current mask, precompute all nonempty submasks of the uncovered targets.
        transitions = [[] for _ in range(size)]
        for mask in range(size):
            rem = full ^ mask
            sub = rem
            while sub:
                transitions[mask].append((mask | sub, sub))
                sub = (sub - 1) & rem

        INF = 10**30
        dp = [INF] * size
        dp[0] = 0

        for x in nums:
            # cost[mask] = minimum increments to make x a multiple of lcm[mask]
            cost = [0] * size
            for mask in range(1, size):
                cost[mask] = (-x) % lcm[mask]

            # Copy dp so the current element is used at most once.
            ndp = dp[:]

            for mask, base in enumerate(dp):
                if base == INF:
                    continue
                for new_mask, sub in transitions[mask]:
                    val = base + cost[sub]
                    if val < ndp[new_mask]:
                        ndp[new_mask] = val

            dp = ndp

            # Costs are nonnegative, so zero is globally optimal.
            if dp[full] == 0:
                return 0

        return dp[full]


if __name__ == "__main__":
    sol = Solution()
    cases = [
        (([1, 2, 3], [4]), 1),
        (([8, 4], [10, 5]), 2),
        (([7, 9, 10], [7]), 0),
        (([60, 1, 1, 1], [2, 3, 4, 5]), 0),
        (([2, 1], [2, 2]), 0),
        (([1, 1], [2, 2]), 1),
        (([5, 1], [1, 2]), 1),
        (([2, 1], [1, 2]), 0),
        (([1, 1, 1, 1], [9991, 9973, 9967, 9949]), 39876),
        (([209, 1, 1, 1], [2, 3, 5, 7]), 1),
        (([5, 1, 1], [6, 10, 15]), 24),
    ]

    ok = True
    for (nums, target), expected in cases:
        got = sol.minimumIncrements(nums, target)
        if got != expected:
            ok = False
            print(f"FAIL nums={nums} target={target} expected={expected} got={got}")

    print("SAMPLE TESTS:", "PASS" if ok else "FAIL")