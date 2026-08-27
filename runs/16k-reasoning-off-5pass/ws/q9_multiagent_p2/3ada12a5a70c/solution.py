from typing import List
from bisect import bisect_right

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        # Helper function to map 2D coordinates to a linear scale along the perimeter
        # Order: Left (0,0)->(0,side), Top (0,side)->(side,side), Right (side,side)->(side,0), Bottom (side,0)->(0,0)
        def get_perimeter(x: int, y: int) -> int:
            if x == 0:
                return y  # Left side
            elif y == side:
                return side + x  # Top side
            elif x == side:
                return 2 * side + (side - y)  # Right side
            else:
                return 3 * side + (side - x)  # Bottom side
        
        # Calculate perimeter length
        perimeter = 4 * side
        
        # Map points to their perimeter positions
        p_vals = [get_perimeter(x, y) for x, y in points]
        
        # Sort the perimeter values
        p_vals.sort()
        n = len(p_vals)
        
        # Duplicate the list to handle circularity easily
        # doubled_p[j] corresponds to p_vals[j % n] + (j // n) * perimeter
        doubled_p = p_vals + [p + perimeter for p in p_vals]
        
        def check(d: int) -> bool:
            # Try starting from each point in the original set
            for i in range(n):
                count = 1
                last_idx = i
                current_pos = p_vals[i]
                
                # Greedily pick next points
                for _ in range(k - 1):
                    target = current_pos + d
                    # Find index of first element >= target
                    # We search in the doubled array starting after the last picked index
                    idx = bisect_right(doubled_p, target, lo=last_idx + 1)
                    
                    # Check if we are still within one full circle traversal from the start.
                    # We need to ensure that the selected points, when mapped back to the original circle,
                    # maintain the distance constraint including the wrap-around.
                    # The condition idx < n + i ensures that the last picked point is strictly before
                    # the point corresponding to p_vals[i] + perimeter in the doubled array.
                    # This prevents selecting a point that would require wrapping around more than once
                    # or selecting the same point instance twice in a way that breaks the circular logic.
                    if idx >= n + i:
                        break
                    
                    last_idx = idx
                    current_pos = doubled_p[idx]
                    count += 1
                
                if count >= k:
                    # Check the wrap-around distance
                    # The last picked point is at index last_idx in doubled_p.
                    # Its value is current_pos.
                    # The first point is at index i, value p_vals[i].
                    # The distance across the boundary is (p_vals[i] + perimeter) - current_pos.
                    wrap_dist = (p_vals[i] + perimeter) - current_pos
                    if wrap_dist >= d:
                        return True
            return False

        # Binary search for the maximum distance
        low = 0
        high = 2 * side  # Max possible Manhattan distance on boundary is 2*side
        ans = 0
        
        while low <= high:
            mid = (low + high) // 2
            if mid == 0:
                ans = max(ans, mid)
                low = mid + 1
                continue
            
            if check(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        
        return ans