from typing import List
from bisect import bisect_right

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        max_r = 0
        for _, r in queries:
            if r > max_r:
                max_r = r

        # powers[i] = 4^i. The last power is strictly greater than max_r.
        powers = [1]
        while powers[-1] <= max_r:
            powers.append(powers[-1] * 4)

        # prefix[i] = sum_{x=1}^{powers[i] - 1} cost(x)
        # Bucket i has cost i and covers [powers[i-1], powers[i] - 1].
        prefix = [0] * len(powers)
        for i in range(1, len(powers)):
            prefix[i] = prefix[i - 1] + (powers[i] - powers[i - 1]) * i

        br = bisect_right

        def prefix_sum(n: int) -> int:
            """Return sum_{x=1}^n cost(x)."""
            if n <= 0:
                return 0
            idx = br(powers, n) - 1
            completed = prefix[idx]
            current_bucket_cost = idx + 1
            current_count = n - powers[idx] + 1
            return completed + current_count * current_bucket_cost

        ans = 0
        for l, r in queries:
            total = prefix_sum(r) - prefix_sum(l - 1)
            mx = br(powers, r)  # cost(r), since cost is nondecreasing
            ans += max((total + 1) // 2, mx)

        return ans