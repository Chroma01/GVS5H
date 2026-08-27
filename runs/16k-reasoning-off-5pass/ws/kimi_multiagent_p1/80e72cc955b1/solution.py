from typing import List


class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def level(x: int) -> int:
            # Number of floor(/4) hits needed to reduce x (>= 1) to 0.
            # L(x) = k+1 for x in [4^k, 4^(k+1) - 1].
            return (x.bit_length() + 1) // 2

        def prefix(n: int) -> int:
            # Sum of level(x) for x in [1, n].
            if n <= 0:
                return 0
            total = 0
            lo = 1          # 4^k
            k = 1           # level value for this bucket
            while lo <= n:
                hi = lo * 4 - 1
                if hi > n:
                    hi = n
                total += k * (hi - lo + 1)
                lo *= 4
                k += 1
            return total

        ans = 0
        for l, r in queries:
            s = prefix(r) - prefix(l - 1)
            ops = (s + 1) // 2
            m = level(r)
            if m > ops:
                ops = m
            ans += ops
        return ans