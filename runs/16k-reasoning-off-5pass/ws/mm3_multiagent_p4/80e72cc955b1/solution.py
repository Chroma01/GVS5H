from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        # Precompute powers of 4 up to > 1e9
        p4 = [1]
        while p4[-1] <= 10**9:
            p4.append(p4[-1] * 4)
        # p4[k] = 4^k, and numbers in [p4[k], p4[k+1)-1] have cost k+1.
        # The maximum exponent we need: we need p4 up to > 1e9 so that p4[-1] > 1e9.
        # We also keep p4[-1] as an upper sentinel.
        
        def cost_range_sum_and_max(l: int, r: int):
            total = 0
            mx = 0
            # iterate over k where bucket [4^k, 4^{k+1}-1] intersects [l, r]
            for k in range(len(p4) - 1):
                lo = max(l, p4[k])
                hi = min(r, p4[k+1] - 1)
                if lo > hi:
                    continue
                cnt = hi - lo + 1
                total += cnt * (k + 1)
                if (k + 1) > mx:
                    mx = k + 1
            return total, mx
        
        ans = 0
        for l, r in queries:
            S, M = cost_range_sum_and_max(l, r)
            # min operations = max(ceil(S/2), M)
            ops = max((S + 1) // 2, M)
            ans += ops
        return ans