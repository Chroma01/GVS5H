from typing import List
import bisect

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        # powers of 4 up to > 1e9: 4^15 = 1073741824
        pow4 = [1]
        while pow4[-1] <= 10**9:
            pow4.append(pow4[-1] * 4)

        # pref[k] = sum_{i=1}^{k} i * 3 * 4^(i-1)
        max_level = len(pow4)
        pref = [0] * (max_level + 1)
        for k in range(1, max_level + 1):
            pref[k] = pref[k - 1] + k * 3 * (4 ** (k - 1))

        def cost(x: int) -> int:
            if x <= 0:
                return 0
            # cost is the number of base-4 digits of x
            return bisect.bisect_right(pow4, x)

        def prefix_cost(n: int) -> int:
            """sum_{x=1}^{n} cost(x)"""
            if n <= 0:
                return 0
            L = bisect.bisect_right(pow4, n)
            # full levels 1..L-1, then part of level L
            return pref[L - 1] + L * (n - pow4[L - 1] + 1)

        total = 0
        for l, r in queries:
            total_cost = prefix_cost(r) - prefix_cost(l - 1)
            max_cost = cost(r)  # cost is nondecreasing
            total += max(max_cost, (total_cost + 1) // 2)

        return total