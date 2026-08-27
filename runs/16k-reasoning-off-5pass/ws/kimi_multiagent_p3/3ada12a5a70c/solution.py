from bisect import bisect_left
from typing import List


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        P = 4 * side

        # Map each boundary point to its arc-length coordinate along the
        # perimeter, starting at (0,0) and going counterclockwise:
        #   bottom edge (y == 0):    pos = x
        #   right edge  (x == side): pos = side + y
        #   top edge    (y == side): pos = 2*side + (side - x)
        #   left edge   (x == 0):    pos = 3*side + (side - y)
        pos = []
        for x, y in points:
            if y == 0:
                pos.append(x)
            elif x == side:
                pos.append(side + y)
            elif y == side:
                pos.append(2 * side + (side - x))
            else:  # x == 0
                pos.append(3 * side + (side - y))
        pos.sort()
        n = len(pos)
        # Doubled array to handle wrap-around on the circle.
        pos2 = pos + [p + P for p in pos]

        def can(D: int) -> bool:
            # Try every point as the fixed start of the greedy selection.
            for s in range(n):
                cnt = 1
                last = pos2[s]
                idx = s
                # Greedily take the next point at arc distance >= D.
                while cnt < k:
                    nxt = bisect_left(pos2, last + D, idx + 1)
                    if nxt >= s + n:
                        break  # wrapped past all available points
                    idx = nxt
                    last = pos2[nxt]
                    cnt += 1
                # Wrap-around gap must also be >= D.
                if cnt >= k and last - pos2[s] <= P - D:
                    return True
            return False

        lo, hi = 1, P // k  # answer <= P/k <= side since k >= 4
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo