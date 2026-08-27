import bisect
from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        # Precompute powers of 4 and prefix sums of heights
        # h(x) = floor(log4(x)) + 1 for x > 0
        # h(x) is constant on [4^k, 4^(k+1)-1] with value k+1
        powers = [1]
        S = [0]  # S[k] stores sum of h(x) for x in [1, 4^k - 1]
        for k in range(1, 16):
            powers.append(powers[-1] * 4)
            # Number of elements in [4^(k-1), 4^k - 1] is 3 * 4^(k-1)
            # Each has height k
            S.append(S[-1] + 3 * powers[-2] * k)
            
        def prefix_sum(x):
            if x == 0:
                return 0
            # Find k such that 4^k <= x < 4^(k+1)
            idx = bisect.bisect_right(powers, x)
            k = idx - 1
            # Sum up to 4^k - 1 is S[k], plus remaining elements in current interval
            return S[k] + (x - powers[k] + 1) * (k + 1)
            
        def max_h(x):
            if x == 0:
                return 0
            # h(x) = k + 1 where 4^k <= x < 4^(k+1)
            return bisect.bisect_right(powers, x)
            
        total_ops = 0
        for l, r in queries:
            s = prefix_sum(r) - prefix_sum(l - 1)
            m = max_h(r)
            # Minimum operations is max(max_height, ceil(sum_heights / 2))
            total_ops += max(m, (s + 1) // 2)
            
        return total_ops