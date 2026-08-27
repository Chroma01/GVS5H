from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        # Map each boundary point to a 1D ring coordinate by walking the square perimeter clockwise.
        # Start at (0,0) -> (side,0) -> (side,side) -> (0,side) -> back to (0,0)
        perim = 4 * side
        coords = []
        for x, y in points:
            if y == 0:
                # bottom edge: (0,0) to (side,0)
                d = x
            elif x == side:
                # right edge: (side,0) to (side,side)
                d = side + y
            elif y == side:
                # top edge: (side,side) to (0,side)
                d = 2 * side + (side - x)
            else:
                # left edge: (0,side) to (0,0)
                d = 3 * side + (side - y)
            coords.append(d)
        coords.sort()
        n = len(coords)
        if n == 0:
            return 0
        
        # Duplicated sorted array for circular handling
        extended = coords + [c + perim for c in coords]
        
        def can_select(D: int) -> bool:
            # Build nxt array: nxt[i] is the smallest index j > i with extended[j] - extended[i] >= D
            nxt = [0] * (2 * n)
            j = 0
            for i in range(2 * n):
                while j < 2 * n and extended[j] - extended[i] < D:
                    j += 1
                nxt[i] = j
            
            # For each starting index in [0, n-1], greedily try to select k points
            for i in range(n):
                idx = i
                ok = True
                for step in range(k - 1):
                    if nxt[idx] >= 2 * n:
                        ok = False
                        break
                    idx = nxt[idx]
                if not ok:
                    continue
                # If we successfully took k points, check span
                if extended[idx] - extended[i] <= perim - D:
                    return True
            return False
        
        # Binary search on D
        lo, hi = 0, perim
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can_select(mid):
                lo = mid
            else:
                hi = mid - 1
        
        return lo