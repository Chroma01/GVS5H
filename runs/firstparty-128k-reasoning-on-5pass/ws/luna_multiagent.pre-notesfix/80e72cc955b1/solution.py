from typing import List


class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def prefix_sum(n: int) -> int:
            """Return the sum of required selections for all x in [1, n]."""
            if n <= 0:
                return 0

            total = 0
            start = 1
            steps = 1

            while start <= n:
                end = start * 4 - 1
                right = min(n, end)
                total += (right - start + 1) * steps
                start *= 4
                steps += 1

            return total

        answer = 0

        for left, right in queries:
            required_selections = prefix_sum(right) - prefix_sum(left - 1)
            answer += (required_selections + 1) // 2

        return answer