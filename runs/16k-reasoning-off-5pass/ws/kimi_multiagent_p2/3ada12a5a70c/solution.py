from typing import List
from bisect import bisect_left

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        # Parameterize each point by its distance along the perimeter from (0,0)
        # going counter-clockwise: (0,0) -> (side,0) -> (side,side) -> (0,side) -> (0,0)
        L = 4 * side
        pos = []
        for x, y in points:
            if y == 0:
                p = x
            elif x == side:
                p = side + y
            elif y == side:
                p = 2 * side + (side - x)
            else:  # x == 0
                p = 3 * side + (side - y)
            pos.append(p)
        
        pos.sort()
        n = len(pos)
        # Duplicate positions + L to handle circular wrap-around
        arr = pos + [p + L for p in pos]
        
        def can(d: int) -> bool:
            # Try each point as the starting point
            for i in range(n):
                start = arr[i]
                cnt = 1
                cur = start
                # Greedily pick the next point at distance >= d
                for _ in range(k - 1):
                    nxt = bisect_left(arr, cur + d)
                    if nxt >= i + n:  # out of our window
                        break
                    if arr[nxt] >= start + L:  # wrapped past full circle
                        break
                    cur = arr[nxt]
                    cnt += 1
                if cnt >= k:
                    return True
            return False
        
        lo, hi = 0, 2 * side
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo