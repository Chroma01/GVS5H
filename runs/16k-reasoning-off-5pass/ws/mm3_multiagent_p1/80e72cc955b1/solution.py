import bisect
from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        # Precompute powers of 4: pow4[k] = 4^k for k = 0..16 (since 4^15 = 1073741824 > 1e9)
        pow4 = []
        p = 1
        for k in range(17):
            pow4.append(p)
            p *= 4
        # pow4[k] = 4^k
        # For x >= 1, f(x) = floor(log4(x)) + 1 = smallest k such that 4^k > x
        # which is bisect_right(pow4, x) since pow4[k] = 4^k
        # But for x=0, f(0)=0 (already zero, no operation needed)
        
        def f(x: int) -> int:
            if x <= 0:
                return 0
            # number of steps to reduce x to 0: smallest k with 4^k > x
            # pow4 is sorted, bisect_right gives insertion point = k
            return bisect.bisect_right(pow4, x)
        
        def sum_f(l: int, r: int) -> int:
            # Sum of f(x) for x in [l, r], l >= 1
            total = 0
            cur = l
            while cur <= r:
                # find k such that pow4[k] <= cur < pow4[k+1]
                k = bisect.bisect_right(pow4, cur) - 1  # since pow4[k] <= cur
                if k < 0:
                    k = 0
                # block upper bound: pow4[k+1] - 1
                block_end = min(pow4[k + 1] - 1, r)
                count = block_end - cur + 1
                total += count * (k + 1)
                cur = block_end + 1
            return total
        
        ans = 0
        for l, r in queries:
            max_steps = f(r)
            total_steps = sum_f(l, r)
            ops = max((total_steps + 1) // 2, max_steps)
            ans += ops
        return ans