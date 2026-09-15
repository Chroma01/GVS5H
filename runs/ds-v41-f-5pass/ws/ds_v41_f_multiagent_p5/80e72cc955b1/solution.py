from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def prefix(n: int) -> int:
            """Sum of d(x) for x = 1..n, where d(x) is the number of
            floor-divisions by 4 needed to reduce x to 0."""
            if n <= 0:
                return 0
            res = 0
            lo = 1      # 4^(k-1)
            k = 1
            while lo <= n:
                hi = lo * 4 - 1   # 4^k - 1
                if hi > n:
                    hi = n
                res += k * (hi - lo + 1)
                lo *= 4
                k += 1
            return res

        total = 0
        for l, r in queries:
            s = prefix(r) - prefix(l - 1)
            total += (s + 1) // 2
        return total