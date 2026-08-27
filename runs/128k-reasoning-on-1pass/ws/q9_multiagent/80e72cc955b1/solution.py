from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        total_ops = 0
        for l, r in queries:
            cost_sum = self.get_cost_sum(r) - self.get_cost_sum(l - 1)
            total_ops += (cost_sum + 1) // 2
        return total_ops

    def get_cost_sum(self, n: int) -> int:
        if n <= 0:
            return 0
        total = 0
        curr = 1
        k = 0
        while curr <= n:
            upper = curr * 4 - 1
            count = min(n, upper) - curr + 1
            total += count * (k + 1)
            curr *= 4
            k += 1
        return total