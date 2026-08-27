from typing import List


class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def prefix_cost(n: int) -> int:
            """Sum required reductions for all values from 1 through n."""
            total = 0
            start = 1
            reductions = 1

            while start <= n:
                end = min(n, start * 4 - 1)
                total += (end - start + 1) * reductions
                start *= 4
                reductions += 1

            return total

        result = 0

        for left, right in queries:
            total_reductions = prefix_cost(right) - prefix_cost(left - 1)
            result += (total_reductions + 1) // 2

        return result