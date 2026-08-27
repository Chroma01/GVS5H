from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        perim = 4 * side
        # map each boundary point to a perimeter coordinate in [0, 4*side)
        per_coords = []
        for x, y in points:
            if y == 0:          # bottom edge: from (0,0) to (side,0)
                p = x
            elif x == side:     # right edge: from (side,0) to (side,side)
                p = side + y
            elif y == side:     # top edge: from (side,side) to (0,side)
                p = 2 * side + (side - x)
            else:               # left edge: from (0,side) to (0,0)
                # x == 0, y < side
                p = 3 * side + (side - y)
            per_coords.append(p)
        per_coords.sort()
        n = len(per_coords)
        # duplicate with +perim to simplify circular handling
        per2 = per_coords + [p + perim for p in per_coords]
        
        def feasible(d: int) -> bool:
            # we need to know if we can select k points with circular distance >= d
            # the total length of the circular interval that the k points must span
            # is at most perim - d (because the gap after the last point back to first must be >= d)
            max_total = perim - d
            
            # precompute next[i]: the smallest index j > i with per2[j] - per2[i] >= d
            # per2 is sorted, so this can be done with two pointers
            # but we only need it for indices in [0, n-1] (original points)
            # and the jumps will go up to i + n (because we can wrap at most once)
            # We'll compute on the fly using two pointers for each start i.
            
            # To speed up, we can precompute next_idx for each i in [0, 2n)
            # next_idx[i] = smallest j > i with per2[j] - per2[i] >= d
            # then chain k-1 jumps
            # But k is small (<=25), so we can just simulate per start.
            
            nxt = [0] * (2 * n)
            j = 0
            for i in range(2 * n):
                while j < 2 * n and per2[j] - per2[i] < d:
                    j += 1
                nxt[i] = j  # may be equal to 2n, meaning no valid next
            
            for i in range(n):
                if nxt[i] >= 2 * n:
                    continue
                # try to take k points starting at i
                cur = i
                ok = True
                for _ in range(k - 1):
                    if nxt[cur] >= 2 * n:
                        ok = False
                        break
                    cur = nxt[cur]
                if not ok:
                    continue
                # After k-1 jumps, the total span from per2[i] to per2[cur] must be <= perim - d
                # because we need the wrap-around gap to be >= d
                if per2[cur] - per2[i] <= perim - d:
                    return True
            return False
        
        # binary search on d
        lo, hi = 0, perim  # inclusive hi? hi is possible answer
        # Actually, maximum possible min distance is perim // 2? No, because we can have up to k points.
        # Upper bound: perim // 2 if k>=2, but we can just use perim.
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo