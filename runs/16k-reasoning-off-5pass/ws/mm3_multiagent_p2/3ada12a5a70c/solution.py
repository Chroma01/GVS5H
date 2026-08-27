from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        L = 4 * side
        # map each boundary point to its 1D position along the perimeter
        perim = []
        for x, y in points:
            if y == 0:               # bottom edge, from (0,0) to (side,0)
                p = x
            elif x == side:          # right edge, from (side,0) to (side,side)
                p = side + y
            elif y == side:          # top edge, from (side,side) to (0,side)
                p = 2 * side + (side - x)
            else:                    # left edge, from (0,side) to (0,0)
                # x == 0 and 0 < y < side
                p = 3 * side + (side - y)
            perim.append(p)
        perim.sort()
        n = len(perim)
        # duplicate with +L to handle wrap-around
        perim2 = perim + [p + L for p in perim]
        
        def feasible(d: int) -> bool:
            # try every point as a possible first pick
            for i in range(n):
                cnt = 1
                cur = perim[i]
                idx = i + 1
                # greedily pick points at distance >= d
                while cnt < k:
                    # find next position with distance >= d from cur
                    nxt = cur + d
                    # binary search in perim2 starting from idx
                    lo, hi = idx, len(perim2)
                    while lo < hi:
                        mid = (lo + hi) // 2
                        if perim2[mid] < nxt:
                            lo = mid + 1
                        else:
                            hi = mid
                    if lo == len(perim2):
                        break
                    cur = perim2[lo]
                    idx = lo + 1
                    cnt += 1
                if cnt >= k:
                    return True
            return False
        
        # binary search on the answer
        lo, hi = 0, L // k + 1  # hi is exclusive upper bound
        while lo < hi:
            mid = (lo + hi) // 2
            if mid == 0:
                lo = 1
                continue
            if feasible(mid):
                lo = mid + 1
            else:
                hi = mid
        return lo - 1