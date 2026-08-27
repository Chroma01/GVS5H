from typing import List
from bisect import bisect_right

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        if not queries:
            return 0

        max_r = max(r for _, r in queries)

        # powers[i] = 4^i, with the last power strictly greater than max_r
        powers = [1]
        while powers[-1] <= max_r:
            powers.append(powers[-1] * 4)

        # pref[i] = sum of d(x) for x in [1, 4^i - 1]
        pref = [0] * len(powers)
        for i in range(1, len(powers)):
            pref[i] = pref[i - 1] + (powers[i] - powers[i - 1]) * i

        def prefix(n: int) -> int:
            """Sum of d(x) for x in [1, n]."""
            if n <= 0:
                return 0
            i = bisect_right(powers, n) - 1
            # d(x) = i + 1 on [4^i, 4^(i+1) - 1]
            return pref[i] + (n - powers[i] + 1) * (i + 1)

        def depth(x: int) -> int:
            """Number of floor divisions by 4 needed to make x zero."""
            return bisect_right(powers, x)

        ans = 0
        for l, r in queries:
            total_depth = prefix(r) - prefix(l - 1)
            max_depth = depth(r)
            ans += max((total_depth + 1) // 2, max_depth)

        return ans