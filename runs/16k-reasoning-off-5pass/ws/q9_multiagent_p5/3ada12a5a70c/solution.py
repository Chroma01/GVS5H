from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        # Helper function to calculate Manhattan distance between two points
        def manhattan_dist(p1: List[int], p2: List[int]) -> int:
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        
        # Helper function to get the perimeter index for sorting
        def get_perimeter_index(p: List[int]) -> int:
            x, y = p
            if y == 0:
                return x
            elif x == side:
                return side + y
            elif y == side:
                return 2 * side + (side - x)
            elif x == 0:
                return 3 * side + (side - y)
            return -1  # Should not happen based on constraints
        
        # Sort points based on their position along the perimeter
        points.sort(key=get_perimeter_index)
        
        # Helper function to check if it's possible to select k points with at least 'dist' separation
        def can_select(dist: int) -> bool:
            if dist == 0:
                return True
            count = 1
            last_idx = 0
            # Iterate through points starting from the second one
            for i in range(1, len(points)):
                if manhattan_dist(points[i], points[last_idx]) >= dist:
                    count += 1
                    last_idx = i
                    if count >= k:
                        return True
            return count >= k
        
        # Binary search for the maximum minimum distance
        low = 0
        high = 2 * side  # Maximum possible Manhattan distance is 2*side
        ans = 0
        
        while low <= high:
            mid = (low + high) // 2
            if mid == 0:
                ans = max(ans, mid)
                low = mid + 1
                continue
            
            if can_select(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
                
        return ans