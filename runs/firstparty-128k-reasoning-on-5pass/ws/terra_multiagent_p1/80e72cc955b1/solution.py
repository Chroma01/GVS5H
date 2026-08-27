from typing import List


class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def prefix_work(n: int) -> int:
            if n <= 0:
                return 0

            total = 0
            start = 1
            divisions = 1

            while start <= n:
                end = min(n, start * 4 - 1)
                total += (end - start + 1) * divisions
                start *= 4
                divisions += 1

            return total

        answer = 0
        for l, r in queries:
            work = prefix_work(r) - prefix_work(l - 1)
            answer += (work + 1) // 2

        return answer