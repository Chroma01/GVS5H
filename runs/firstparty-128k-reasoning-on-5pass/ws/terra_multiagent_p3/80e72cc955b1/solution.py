from typing import List


class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def prefix_depth_sum(x: int) -> int:
            if x <= 0:
                return 0

            total = 0
            start = 1
            depth = 1

            while start <= x:
                end = start * 4 - 1
                count = min(x, end) - start + 1
                total += count * depth
                start *= 4
                depth += 1

            return total

        answer = 0
        for l, r in queries:
            required_reductions = prefix_depth_sum(r) - prefix_depth_sum(l - 1)
            answer += (required_reductions + 1) // 2

        return answer