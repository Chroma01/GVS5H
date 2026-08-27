from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        n = len(points)
        # Precompute perimeter coordinates and store (perimeter, x, y)
        # Perimeter path: (0,0) -> (side,0) -> (side,side) -> (0,side) -> (0,0)
        # Bottom: (x, 0) -> p = x
        # Right: (side, y) -> p = side + y
        # Top: (x, side) -> p = 2*side + (side - x) = 3*side - x
        # Left: (0, y) -> p = 3*side + (side - y) = 4*side - y
        
        pts = []
        for x, y in points:
            if y == 0:
                p = x
            elif x == side:
                p = side + y
            elif y == side:
                p = 3 * side - x
            else: # x == 0
                p = 4 * side - y
            pts.append((p, x, y))
        
        # Sort by perimeter coordinate
        pts.sort(key=lambda x: x[0])
        
        # Duplicate to handle wrap-around easily
        pts += pts
        
        def check(d: int) -> bool:
            # Try to pick k points with min distance >= d
            # We try starting at each of the first n points
            for start in range(n):
                curr = start
                count = 1
                # We need to pick k-1 more points
                for _ in range(k - 1):
                    # Find the smallest index 'next' > curr such that manhattan(curr, next) >= d
                    # The set of points with manhattan < d forms a contiguous segment [curr+1, end]
                    # So we can binary search for the first point where dist >= d
                    
                    low = curr + 1
                    high = curr + n # Search within one full cycle
                    
                    # Binary search for the first index where dist >= d
                    # Predicate: dist < d is True for the "bad" segment, False otherwise.
                    # Since the bad segment is contiguous, this predicate is monotonic (True...True False...False)
                    while low < high:
                        mid = (low + high) // 2
                        # Calculate Manhattan distance
                        x1, y1 = pts[curr][1], pts[curr][2]
                        x2, y2 = pts[mid][1], pts[mid][2]
                        dist = abs(x1 - x2) + abs(y1 - y2)
                        
                        if dist < d:
                            low = mid + 1
                        else:
                            high = mid
                    
                    if low >= curr + n:
                        # No valid point found within the cycle
                        break
                    
                    curr = low
                    count += 1
                
                if count == k:
                    return True
            return False

        # Binary search for the answer
        low = 1
        high = 2 * side # Max possible Manhattan distance on boundary is 2*side
        ans = 0
        
        while low <= high:
            mid = (low + high) // 2
            if mid == 0:
                low = 1
                continue
            if check(mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        
        return ans