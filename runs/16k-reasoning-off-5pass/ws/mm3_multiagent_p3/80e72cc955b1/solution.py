from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        # Helper: total depth sum for numbers in [1, r]
        # Depth of x is floor(log4(x)) + 1 (1-indexed)
        def calc(r: int) -> int:
            if r <= 0:
                return 0
            total = 0
            p = 1  # 4^0
            k = 1  # current depth level
            while p <= r:
                nxt = p * 4
                # Count numbers in [p, nxt-1] that are <= r
                hi = min(r, nxt - 1)
                cnt = hi - p + 1
                if cnt > 0:
                    total += k * cnt
                p = nxt
                k += 1
            return total

        def total_depth(l: int, r: int) -> int:
            return calc(r) - calc(l - 1)

        def max_depth(r: int) -> int:
            # depth of the largest number r: floor(log4(r)) + 1
            d = 0
            p = 1
            while p <= r:
                p *= 4
                d += 1
            return d

        ans = 0
        for l, r in queries:
            td = total_depth(l, r)
            md = max_depth(r)
            # operations = max(md, ceil(td / 2)) = max(md, (td + 1) // 2)
            ops = max(md, (td + 1) // 2)
            ans += ops
        return ans