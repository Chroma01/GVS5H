from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def calc(n: int) -> int:
            if n <= 0:
                return 0
            total = 0
            p = 1  # Represents 4^(k-1)
            while p <= n:
                # Count numbers x in [1, n] such that f(x) >= k
                # f(x) >= k <=> x >= 4^(k-1) = p
                # So we count numbers in [p, n]
                count = max(0, n - p + 1)
                total += count
                p *= 4
            return total
        
        ans = 0
        for l, r in queries:
            # The sum of f(x) for x in [l, r] is calc(r) - calc(l-1)
            # Each operation reduces the total sum of f(x) by exactly 2.
            # So operations = (sum) / 2
            total_ops = (calc(r) - calc(l - 1)) // 2
            ans += total_ops
        return ans