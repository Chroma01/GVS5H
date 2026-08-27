from typing import List
from bisect import bisect_right


class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        queries = list(queries)
        if not queries:
            return 0

        max_r = max(r for _, r in queries)

        powers: List[int] = []
        p = 1
        while p <= max_r:
            powers.append(p)
            p *= 4

        prefix: List[int] = [0]
        for p in powers:
            prefix.append(prefix[-1] + p)

        def sum_depths_upto(n: int) -> int:
            if n <= 0:
                return 0
            k = bisect_right(powers, n)
            return k * (n + 1) - prefix[k]

        def depth(n: int) -> int:
            return bisect_right(powers, n)

        ans = 0
        for l, r in queries:
            total = sum_depths_upto(r) - sum_depths_upto(l - 1)
            ans += max(depth(r), (total + 1) // 2)
        return ans