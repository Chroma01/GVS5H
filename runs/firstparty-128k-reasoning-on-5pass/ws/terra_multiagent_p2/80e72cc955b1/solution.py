from typing import List


class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def workload_prefix(x: int) -> int:
            """Sum of division-by-4 workloads for every integer in [1, x]."""
            if x <= 0:
                return 0

            total = 0
            start = 1
            depth = 1

            while start <= x:
                end = min(x, start * 4 - 1)
                total += (end - start + 1) * depth
                start *= 4
                depth += 1

            return total

        def depth(x: int) -> int:
            """Number of divisions by 4 required to turn x into zero."""
            result = 0
            while x:
                x //= 4
                result += 1
            return result

        answer = 0
        for left, right in queries:
            total_work = workload_prefix(right) - workload_prefix(left - 1)
            answer += max((total_work + 1) // 2, depth(right))

        return answer