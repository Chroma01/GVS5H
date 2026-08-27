from typing import List
import math

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        
        def canAchieve(T: int) -> bool:
            # Compute required visits for each position
            need = [0] * n
            for i in range(n):
                need[i] = max(1, (T + points[i] - 1) // points[i])
            
            # The walk starts at -1, first move goes to index 0.
            # Index 0 is the leftmost visited position and has odd visit count.
            # All other positions have even visit counts.
            # Total moves = 2 * sum(need) - 1
            # because index 0 is visited `need[0]` times, but the first visit
            # costs 1 move (not 2), so we subtract 1.
            total = 2 * sum(need) - 1
            return total <= m
        
        # Binary search on answer
        lo, hi = 0, max(points) * m
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if canAchieve(mid):
                lo = mid
            else:
                hi = mid - 1
        
        return lo