from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        # Precompute powers of 4: 4^0, 4^1, ..., up to > 1e9
        pow4 = [1]
        while pow4[-1] <= 10**9:
            pow4.append(pow4[-1] * 4)
        # pow4 = [1, 4, 16, ..., 4^15, 4^16]; 4^15 = 1073741824 > 1e9

        def depth(x: int) -> int:
            # number of times x must be floor-divided by 4 to reach 0 (x >= 1)
            d = 0
            while x:
                x //= 4
                d += 1
            return d

        def range_depth_sum(l: int, r: int) -> int:
            # sum of depth(x) for x in [l, r]; depth = k+1 on [4^k, 4^(k+1)-1]
            total = 0
            k = 0
            while pow4[k] <= r:
                lo = max(l, pow4[k])
                hi = min(r, pow4[k + 1] - 1)
                if lo <= hi:
                    total += (hi - lo + 1) * (k + 1)
                k += 1
            return total

        ans = 0
        for l, r in queries:
            s = range_depth_sum(l, r)
            mx = depth(r)  # depth is non-decreasing, so max is at r
            ans += max(mx, (s + 1) // 2)
        return ans