class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        def get_perimeter_pos(p):
            x, y = p
            if y == 0:
                return x
            elif x == side:
                return side + y
            elif y == side:
                return 2 * side + (side - x)
            else:  # x == 0
                return 3 * side + (side - y)
        
        # Map each point to (perimeter_pos, x, y)
        mapped = []
        for p in points:
            mapped.append((get_perimeter_pos(p), p[0], p[1]))
        
        # Sort by perimeter position
        mapped.sort(key=lambda x: x[0])
        
        n = len(mapped)
        perimeter = 4 * side
        
        # Check if it's possible to select k points with min Manhattan distance >= d
        def check(d):
            # Extended list to handle circular nature
            # We only need to consider starting from each of the original n points
            # and then greedily pick the next point that is at least d away in Manhattan distance
            
            # Precompute the extended list: original points + first n-1 points with perimeter + perimeter
            ext = mapped + [(mapped[i][0] + perimeter, mapped[i][1], mapped[i][2]) for i in range(n - 1)]
            
            for start in range(n):
                count = 1
                last_x, last_y = mapped[start][1], mapped[start][2]
                # Start searching from the next point after start in the extended list
                idx = start + 1
                while idx < len(ext) and count < k:
                    x, y = ext[idx][1], ext[idx][2]
                    # Manhattan distance
                    dist = abs(last_x - x) + abs(last_y - y)
                    if dist >= d:
                        count += 1
                        last_x, last_y = x, y
                    idx += 1
                if count >= k:
                    return True
            return False
        
        # Binary search for the maximum d
        lo, hi = 0, 4 * side
        ans = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            if check(mid):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        
        return ans