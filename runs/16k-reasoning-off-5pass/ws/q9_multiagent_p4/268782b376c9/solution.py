from math import ceil
from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        # Binary search for the maximum possible minimum score
        low = 0
        # Upper bound: Even if we only had 1 index, max score is m * max(points).
        # With n indices, the minimum cannot exceed the average, but a safe upper bound 
        # is simply the max possible score at a single index if we ignored others, 
        # which is m * max(points) = 10^9 * 10^6 = 10^15.
        high = 10**15 
        ans = 0
        
        while low <= high:
            mid = (low + high) // 2
            if mid == 0:
                ans = max(ans, mid)
                low = mid + 1
                continue
            
            if self.can_achieve(points, m, mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        
        return ans

    def can_achieve(self, points: List[int], m: int, target: int) -> bool:
        moves_needed = 0
        n = len(points)
        
        # We start at index -1.
        # We need to visit indices 0, 1, ..., n-1 in order.
        # For each index i, we need to accumulate 'target' points.
        # Number of visits needed at index i: k = ceil(target / points[i])
        # Cost to reach index i from i-1: 1 move.
        # Cost to make additional visits at index i: 2 moves per visit (go to i-1, come back to i).
        # Total moves for index i = 1 + (k - 1) * 2.
        
        for i in range(n):
            # Calculate visits needed: ceil(target / points[i])
            # Using integer arithmetic: (target + points[i] - 1) // points[i]
            k = (target + points[i] - 1) // points[i]
            
            # Cost calculation:
            # First visit: 1 move (from previous index, starting at -1 for i=0)
            # Subsequent (k-1) visits: 2 moves each (back and forth)
            cost = 1 + (k - 1) * 2
            moves_needed += cost
            
            if moves_needed > m:
                return False
        
        return moves_needed <= m