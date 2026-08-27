from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        # Helper to calculate Manhattan distance
        def manhattan_dist(p1: List[int], p2: List[int]) -> int:
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        
        # Map points to perimeter coordinates and keep original coordinates
        # Perimeter order: (0,0) -> (side,0) -> (side,side) -> (0,side) -> (0,0)
        # Side 1: y=0, x from 0 to side. Length: side
        # Side 2: x=side, y from 0 to side. Length: side
        # Side 3: y=side, x from side to 0. Length: side
        # Side 4: x=0, y from side to 0. Length: side
        
        perimeter_points = []
        for x, y in points:
            if y == 0:
                # Bottom side: (0,0) to (side,0)
                p = x
            elif x == side:
                # Right side: (side,0) to (side,side)
                p = side + y
            elif y == side:
                # Top side: (side,side) to (0,side)
                p = 2 * side + (side - x)
            else:
                # Left side: (0,side) to (0,0)
                p = 3 * side + (side - y)
            perimeter_points.append((p, x, y))
        
        # Sort by perimeter coordinate
        perimeter_points.sort(key=lambda x: x[0])
        
        # Extract coordinates for easy access
        # coords[i] = (perimeter_index, x, y)
        coords = perimeter_points
        n = len(coords)
        
        # Binary search for the maximum minimum distance
        low = 0
        high = 2 * side  # Max possible Manhattan distance is 2*side
        ans = 0
        
        while low <= high:
            mid = (low + high) // 2
            if mid == 0:
                ans = max(ans, mid)
                low = mid + 1
                continue
            
            # Check function: can we select k points with min distance >= mid?
            # dp[j] = minimum perimeter index of the j-th point in the selected sequence
            # Initialize with infinity
            dp = [float('inf')] * (k + 1)
            
            # We can start a chain with any point. 
            # To maximize the chance of picking k points, we want the first point to be as early as possible.
            # So dp[1] should be 0 (the first point in sorted order).
            # However, strictly speaking, we could start with any point. 
            # But since we process points in order, if we start with point i > 0, 
            # we are just skipping points 0..i-1. Since we want to fit k points, 
            # starting earlier (index 0) is always better or equal to starting later.
            dp[1] = 0
            
            # We iterate through all points to try and extend chains
            for i in range(1, n):
                # Try to update dp[j] for j from k down to 2
                # We iterate downwards to avoid using the updated dp[j-1] from the current i
                for j in range(k, 1, -1):
                    prev_idx = dp[j-1]
                    if prev_idx != float('inf'):
                        # Check distance between point at prev_idx and current point i
                        # coords is a list of tuples (p, x, y)
                        p_prev = coords[prev_idx]
                        p_curr = coords[i]
                        dist = abs(p_curr[1] - p_prev[1]) + abs(p_curr[2] - p_prev[2])
                        
                        if dist >= mid:
                            if i < dp[j]:
                                dp[j] = i
            
            if dp[k] != float('inf'):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
                
        return ans