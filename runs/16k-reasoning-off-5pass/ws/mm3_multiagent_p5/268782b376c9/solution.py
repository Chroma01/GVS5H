from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        def min_moves(need):
            n = len(need)
            if n == 1:
                return need[0]
            
            # Case 1: Walk ends at position 0
            f = [0] * (n - 1)
            f[n-2] = need[n-1]
            for i in range(n-3, -1, -1):
                f[i] = max(0, need[i+1] - f[i+1])
            if f[0] < need[0] - 1:
                f[0] = need[0] - 1
                for i in range(1, n-1):
                    if f[i-1] + f[i] < need[i]:
                        f[i] = need[i] - f[i-1]
            cost0 = 1 + 2 * sum(f)
            
            # Case 2: Walk ends at position n-1
            f = [0] * (n - 1)
            f[n-2] = need[n-1]
            for i in range(n-3, -1, -1):
                f[i] = max(0, need[i+1] + 1 - f[i+1])
            if f[0] < need[0]:
                f[0] = need[0]
                for i in range(1, n-1):
                    if f[i-1] + f[i] < need[i] + 1:
                        f[i] = need[i] + 1 - f[i-1]
            cost1 = 1 + 2 * sum(f) - (n - 1)
            
            return min(cost0, cost1)
        
        # Binary search on the answer
        lo, hi = 0, max(points) * m
        while lo < hi:
            mid = (lo + hi + 1) // 2
            need = [(mid + p - 1) // p for p in points]
            if min_moves(need) <= m:
                lo = mid
            else:
                hi = mid - 1
        return lo