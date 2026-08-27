from typing import List


class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def prefix(n: int) -> int:
            """Return sum of floor(log_4(x)) + 1 for 1 <= x <= n."""
            if n <= 0:
                return 0

            total = 0
            start = 1
            steps = 1

            while start <= n:
                end = min(n, start * 4 - 1)
                total += (end - start + 1) * steps
                start *= 4
                steps += 1

            return total

        answer = 0
        for left, right in queries:
            required = prefix(right) - prefix(left - 1)
            answer += (required + 1) // 2

        return answer