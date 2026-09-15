from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        perimeter = 4 * side

        # Map each boundary point to its clockwise perimeter coordinate in [0, 4*side).
        # Corner precedence: bottom, right, top, left, so each corner is used once.
        coords = []
        for x, y in points:
            if y == 0:
                t = x
            elif x == side:
                t = side + y
            elif y == side:
                t = 3 * side - x
            else:
                t = 4 * side - y
            coords.append(t)

        coords.sort()
        n = len(coords)

        # For k >= 4 the answer is at most side.
        # Also, if k circular gaps are at least d, then k*d <= perimeter.
        hi = min(side, perimeter // k)
        if hi == 0:
            return 0

        # Doubled array with the second copy shifted by one full perimeter.
        arr = coords + [c + perimeter for c in coords]
        m = 2 * n
        steps = range(k - 1)

        def can(d: int) -> bool:
            if d == 0:
                return True

            # nxt[i] = first index j > i with arr[j] - arr[i] >= d.
            nxt = [0] * m
            j = 0
            a = arr
            for i in range(m):
                if j <= i:
                    j = i + 1
                target = a[i] + d
                while j < m and a[j] < target:
                    j += 1
                nxt[i] = j

            # Try every point as the first selected point in circular order.
            nn = n
            for i in range(nn):
                pos = i
                end = i + nn  # same physical point after one full perimeter

                for _ in steps:
                    pos = nxt[pos]
                    if pos >= end:
                        break
                else:
                    # Final wrap-around gap from last selected point back to start.
                    if a[end] - a[pos] >= d:
                        return True

            return False

        lo = 0
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can(mid):
                lo = mid
            else:
                hi = mid - 1

        return lo