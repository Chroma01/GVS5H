from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        
        def canAchieve(ans: int) -> bool:
            # Compute required visits for each cell: need[i] = ceil(ans / points[i])
            need = [(ans + points[i] - 1) // points[i] for i in range(n)]
            
            # Find the rightmost cell that needs at least one visit
            r = n - 1
            while r >= 0 and need[r] == 0:
                r -= 1
            
            # If no cell needs a visit, we can achieve this with 0 moves
            if r < 0:
                return True
            
            # Simulate the optimal left-to-right sweep
            # visits_next: number of visits that will be given to the next cell from round trips
            visits_next = 0
            # Start with the first move from index -1 to 0
            total_moves = 1
            
            # Sweep from cell 0 to cell r-1
            for i in range(r):
                # When we arrive at cell i, we have 1 visit (the arrival) plus visits_next from previous round trips
                visits_i = 1 + visits_next
                if visits_i < need[i]:
                    # We need more visits; do round trips between i and i+1
                    extra = need[i] - visits_i
                    total_moves += 2 * extra  # each round trip costs 2 moves
                    visits_next = extra      # these visits go to cell i+1
                else:
                    visits_next = 0
                # Move from cell i to cell i+1
                total_moves += 1
            
            # Now we are at cell r
            visits_r = 1 + visits_next
            if visits_r < need[r]:
                # Need more visits at the last cell; do round trips between r-1 and r
                extra = need[r] - visits_r
                total_moves += 2 * extra
            
            return total_moves <= m
        
        # Binary search for the maximum achievable minimum score
        # Upper bound: if we only visit the cell with the maximum points repeatedly,
        # the maximum possible score is max(points) * m
        lo, hi = 0, max(points) * m
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if canAchieve(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo