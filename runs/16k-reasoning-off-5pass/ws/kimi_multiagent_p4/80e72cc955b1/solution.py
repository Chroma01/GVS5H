from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        # Precompute powers of 4 up to > 1e9
        pow4 = [1]
        while pow4[-1] <= 10**9:
            pow4.append(pow4[-1] * 4)
        # pow4 = [1, 4, 16, ..., 4^15, 4^16]; 4^15 = 1073741824 > 1e9

        def depth(x: int) -> int:
            # smallest k such that x < 4^k  (x >= 1)
            k = 0
            while pow4[k] <= x:
                k += 1
            return k

        def range_depth_sum(l: int, r: int) -> int:
            # sum of d(x) for x in [l, r]; d(x) = k for x in [4^(k-1), 4^k - 1]
            total = 0
            k = 1
            while pow4[k - 1] <= r:
                lo = max(l, pow4[k - 1])
                hi = min(r, pow4[k] - 1)
                if lo <= hi:
                    total += k * (hi - lo + 1)
                k += 1
            return total

        ans = 0
        for l, r in queries:
            s = range_depth_sum(l, r)
            mx = depth(r)  # d is nondecreasing, so max depth in [l, r] is d(r)
            ans += max((s + 1) // 2, mx)
        return ans