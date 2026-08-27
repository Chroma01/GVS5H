from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        
        # Binary search for the maximum possible minimum score
        # Range: [0, m] because each move adds at least 1 point (since points[i] >= 1)
        low = 0
        high = m
        ans = 0
        
        while low <= high:
            mid = (low + high) // 2
            
            if mid == 0:
                # If target is 0, it's always possible (0 moves needed)
                ans = max(ans, mid)
                low = mid + 1
                continue
            
            # Calculate required visits for each index to achieve at least 'mid' score
            # req[i] = ceil(mid / points[i])
            # Using integer arithmetic: (mid + points[i] - 1) // points[i]
            req = [(mid + p - 1) // p for p in points]
            
            # Calculate minimum moves required to satisfy all requirements
            # Formula: moves = (n - 1) + 2 * sum(max(0, req[i+1] - req[i])) for i in 0..n-2
            # This formula accounts for the base traversal cost and the extra back-and-forth moves
            # needed when subsequent indices have higher requirements.
            moves = n - 1
            for i in range(n - 1):
                if req[i+1] > req[i]:
                    moves += 2 * (req[i+1] - req[i])
            
            # Check if the calculated moves are within the allowed limit m
            if moves <= m:
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
                
        return ans