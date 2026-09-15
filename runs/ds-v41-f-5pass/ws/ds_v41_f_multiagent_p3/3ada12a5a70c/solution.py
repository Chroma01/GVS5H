from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        S = side
        L = 4 * S
        n = len(points)

        def get_coord(x: int, y: int) -> int:
            # canonical clockwise perimeter coordinate in [0, 4S)
            if y == 0:
                return x                      # bottom edge
            if x == S:
                return S + y                  # right edge
            if y == S:
                return 2 * S + (S - x)        # top edge
            return 3 * S + (S - y)            # left edge

        coords = sorted(get_coord(x, y) for x, y in points)
        A = coords + [c + L for c in coords]   # doubled for circular handling

        def feasible(D: int) -> bool:
            m = 2 * n
            # nxt[i] = smallest j > i with A[j] - A[i] >= D
            nxt = [m] * m
            j = 0
            for i in range(m):
                if j <= i:
                    j = i + 1
                ai = A[i]
                while j < m and A[j] - ai < D:
                    j += 1
                nxt[i] = j

            # For each starting point, greedily take the earliest compatible point.
            for s in range(n):
                limit = s + n                 # window [s, s+n) covers exactly the n distinct points once
                cur = s
                ok = True
                for _ in range(k - 1):
                    cur = nxt[cur]
                    if cur >= limit:
                        ok = False
                        break
                if ok and nxt[cur] <= limit:  # wrap-around gap from last back to start must be >= D
                    return True
            return False

        lo, hi = 0, S                          # for k >= 4 answer <= S by pigeonhole
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo