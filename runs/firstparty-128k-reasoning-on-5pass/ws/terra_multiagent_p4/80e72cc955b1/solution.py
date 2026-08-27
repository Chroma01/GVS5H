from typing import List


class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def prefix_steps(x: int) -> int:
            if x <= 0:
                return 0

            total = 0
            power = 1
            steps = 1

            while power <= x:
                block_end = power * 4 - 1
                count = min(x, block_end) - power + 1
                total += count * steps
                power *= 4
                steps += 1

            return total

        def required_steps(x: int) -> int:
            steps = 0
            power = 1

            while power <= x:
                steps += 1
                power *= 4

            return steps

        answer = 0

        for l, r in queries:
            total_reductions = prefix_steps(r) - prefix_steps(l - 1)
            maximum_reductions = required_steps(r)
            answer += max(maximum_reductions, (total_reductions + 1) // 2)

        return answer