from typing import List


class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def prefix(n: int) -> int:
            if n <= 0:
                return 0

            total = 0
            left = 1
            steps = 1
            power = 4

            while left <= n:
                right = min(n, power - 1)
                total += (right - left + 1) * steps
                left = power
                power *= 4
                steps += 1

            return total

        result = 0

        for left, right in queries:
            work = prefix(right) - prefix(left - 1)
            result += (work + 1) // 2

        return result