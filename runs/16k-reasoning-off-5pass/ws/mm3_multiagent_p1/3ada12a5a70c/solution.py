class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        def to_perimeter(p):
            x, y = p
            if y == 0:          # bottom side: from (0,0) to (side,0)
                return x
            elif x == side:     # right side: from (side,0) to (side,side)
                return side + y
            elif y == side:     # top side: from (side,side) to (0,side)
                return 2 * side + (side - x)
            else:               # left side: from (0,side) to (0,0)
                return 3 * side + (side - y)
        
        coords = sorted(to_perimeter(p) for p in points)
        C = 4 * side
        n = len(coords)
        
        # Precompute the extended coordinates: coords + [c + C for c in coords]
        ext = coords + [c + C for c in coords]
        
        def can_place(D):
            # Try each starting point
            for start in range(n):
                # Greedy: place k points starting at ext[start]
                positions = [ext[start]]
                idx = start
                for _ in range(1, k):
                    # Find the next point with coordinate >= positions[-1] + D
                    target = positions[-1] + D
                    # Binary search in ext for the first coordinate >= target
                    lo, hi = idx + 1, 2 * n
                    while lo < hi:
                        mid = (lo + hi) // 2
                        if ext[mid] >= target:
                            hi = mid
                        else:
                            lo = mid + 1
                    if lo == 2 * n:
                        # No more points available in the extended range
                        break
                    positions.append(ext[lo])
                    idx = lo
                if len(positions) == k:
                    # Check the circular distance from the last placed point back to the start
                    # The last point is positions[-1], the start is ext[start]
                    # Clockwise distance from last to start: ext[start] + C - positions[-1]
                    # This must be >= D
                    if ext[start] + C - positions[-1] >= D:
                        return True
            return False
        
        # Binary search on the answer
        lo, hi = 0, C
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can_place(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo