from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        # Precompute powers of 4: bands are [4^(k-1), 4^k - 1], needing k hits.
        # r <= 1e9 < 4^15, so 16 powers are more than enough.
        pow4 = [1]
        while pow4[-1] <= 10**9:
            pow4.append(pow4[-1] * 4)
        # pow4 = [1, 4, 16, ..., 4^15]

        total_ops = 0
        for l, r in queries:
            hits = 0
            # Band k (1-indexed): numbers x with pow4[k-1] <= x <= pow4[k] - 1 need k hits.
            for k in range(1, len(pow4)):
                lo = pow4[k - 1]
                hi = pow4[k] - 1
                if lo > r:
                    break
                left = l if l > lo else lo
                right = r if r < hi else hi
                if left <= right:
                    hits += k * (right - left + 1)
            total_ops += (hits + 1) // 2
        return total_ops