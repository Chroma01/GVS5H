from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def hits(x: int) -> int:
            # Number of times x must be chosen before floor(x / 4) becomes 0.
            # Equals floor(log4(x)) + 1 for x >= 1.
            return (x.bit_length() + 1) // 2

        def prefix_hits(n: int) -> int:
            # Sum of hits(x) for all 1 <= x <= n.
            if n <= 0:
                return 0
            total = 0
            start = 1
            h = 1
            while start <= n:
                end = start * 4 - 1
                if end > n:
                    end = n
                total += (end - start + 1) * h
                start *= 4
                h += 1
            return total

        answer = 0
        for l, r in queries:
            total_hits = prefix_hits(r) - prefix_hits(l - 1)
            by_pairs = (total_hits + 1) // 2
            by_max = hits(r)
            answer += by_max if by_max >= by_pairs else by_pairs
        return answer