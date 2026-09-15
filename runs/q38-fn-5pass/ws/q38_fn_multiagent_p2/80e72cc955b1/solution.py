from typing import List
from bisect import bisect_right

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        if not queries:
            return 0

        max_r = max(r for _, r in queries)

        # Thresholds where steps(x) increases:
        # steps(x) = k for 4^(k-1) <= x <= 4^k - 1.
        powers = []
        p = 1
        while p <= max_r:
            powers.append(p)
            p *= 4

        def steps(x: int) -> int:
            # Number of thresholds 4^i that are <= x.
            return bisect_right(powers, x)

        def prefix_steps(x: int) -> int:
            # Sum_{v=1..x} steps(v).
            # Each threshold p contributes 1 to steps(v) for every v >= p.
            if x <= 0:
                return 0

            total = 0
            for p in powers:
                if p > x:
                    break
                total += x - p + 1
            return total

        ans = 0
        for l, r in queries:
            total_steps = prefix_steps(r) - prefix_steps(l - 1)
            max_step = steps(r)
            ans += max(max_step, (total_steps + 1) // 2)

        return ans