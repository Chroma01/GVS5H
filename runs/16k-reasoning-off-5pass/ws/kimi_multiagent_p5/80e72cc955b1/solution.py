from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def prefix_sum(n: int) -> int:
            # Sum of base-4 digit counts for all numbers from 1 to n
            if n <= 0:
                return 0
            total = 0
            power = 1  # 4^k
            k = 0
            while power <= n:
                next_power = power * 4
                # Numbers in [power, min(next_power - 1, n)] need k+1 steps
                upper = min(next_power - 1, n)
                count = upper - power + 1
                total += count * (k + 1)
                power = next_power
                k += 1
            return total

        result = 0
        for l, r in queries:
            steps = prefix_sum(r) - prefix_sum(l - 1)
            result += (steps + 1) // 2
        return result