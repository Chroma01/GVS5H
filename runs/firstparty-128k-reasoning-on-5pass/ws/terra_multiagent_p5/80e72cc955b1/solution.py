from typing import List


class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def prefix_workload(n: int) -> int:
            if n <= 0:
                return 0

            total = 0
            start = 1
            workload = 1

            while start <= n:
                end = start * 4 - 1
                count = min(n, end) - start + 1
                total += count * workload
                start *= 4
                workload += 1

            return total

        def workload_of(x: int) -> int:
            workload = 0
            while x > 0:
                workload += 1
                x //= 4
            return workload

        answer = 0

        for l, r in queries:
            total_workload = prefix_workload(r) - prefix_workload(l - 1)
            maximum_workload = workload_of(r)
            answer += max(maximum_workload, (total_workload + 1) // 2)

        return answer