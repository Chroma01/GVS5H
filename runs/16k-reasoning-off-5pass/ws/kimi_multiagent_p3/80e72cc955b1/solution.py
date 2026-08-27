from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        # Precompute powers of 4: POW4[k] = 4^k
        # Numbers x with depth exactly k satisfy 4^(k-1) <= x <= 4^k - 1,
        # where depth(x) = number of floor(/4) operations to reduce x to 0.
        POW4 = [1]
        while POW4[-1] <= 10**9:
            POW4.append(POW4[-1] * 4)
        # POW4 = [1, 4, 16, ..., 4^15] since 4^15 = 1073741824 > 1e9

        total = 0
        for l, r in queries:
            sum_depths = 0
            max_depth = 0
            # depth k covers [4^(k-1), 4^k - 1]
            for k in range(1, len(POW4)):
                lo = POW4[k - 1]
                if lo > r:
                    break
                hi = POW4[k] - 1
                left = l if l > lo else lo
                right = r if r < hi else hi
                if left <= right:
                    cnt = right - left + 1
                    sum_depths += cnt * k
                    max_depth = k  # largest depth present in [l, r]
            # Min operations = max(max_depth, ceil(sum_depths / 2))
            ops = (sum_depths + 1) // 2
            if max_depth > ops:
                ops = max_depth
            total += ops
        return total