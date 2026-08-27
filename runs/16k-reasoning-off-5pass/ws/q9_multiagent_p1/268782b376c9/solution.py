from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        def check(target: int) -> bool:
            total_moves = 0
            n = len(points)
            for i in range(n):
                # Moves to reach index i for the first time from -1
                # Path: -1 -> 0 -> ... -> i (i+1 steps)
                moves_to_reach = i + 1
                
                # Points obtained on first visit
                current_points = points[i]
                needed = target - current_points
                
                if needed > 0:
                    # Calculate extra visits needed (ceiling division)
                    # Each extra visit costs 2 moves (go away and come back)
                    # e.g., i -> i+1 -> i or i -> i-1 -> i
                    visits_needed = (needed + current_points - 1) // current_points
                    extra_moves = visits_needed * 2
                    moves_to_reach += extra_moves
                
                total_moves += moves_to_reach
                if total_moves > m:
                    return False
            return total_moves <= m

        # Binary search for the maximum possible minimum score
        low = 0
        # Upper bound estimation:
        # Max points per index is 10^6.
        # Max moves is 10^9.
        # A safe upper bound is 10^15, which covers m * max(points) roughly.
        high = 10**15 
        
        ans = 0
        while low <= high:
            mid = (low + high) // 2
            if check(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        
        return ans