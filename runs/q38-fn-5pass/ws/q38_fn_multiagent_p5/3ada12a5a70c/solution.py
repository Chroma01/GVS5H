from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        C = 4 * side

        # Map each boundary point to its coordinate on the square perimeter.
        # The perimeter is treated as a circle of circumference 4 * side.
        coords = []
        for x, y in points:
            if y == 0:
                t = x
            elif x == side:
                t = side + y
            elif y == side:
                t = 2 * side + (side - x)
            else:
                t = 3 * side + (side - y)
            coords.append(t)

        coords.sort()
        n = len(coords)

        # Duplicated coordinates handle circular wraparound.
        arr = coords + [t + C for t in coords]
        m = 2 * n

        def feasible(d: int) -> bool:
            if d == 0:
                return True

            # nxt[i] = first index j > i with arr[j] - arr[i] >= d.
            nxt = [0] * m
            j = 0
            a = arr
            mm = m
            dd = d

            for i in range(mm):
                if j <= i:
                    j = i + 1
                ai = a[i]
                while j < mm and a[j] - ai < dd:
                    j += 1
                nxt[i] = j

            limit = C - d
            steps = range(k - 1)
            nx = nxt
            aa = a

            # Try every original point as the first selected point in circular order.
            for i in range(n):
                pos = i
                for _ in steps:
                    pos = nx[pos]
                    if pos >= mm:
                        break
                else:
                    # The final wraparound gap back to point i must also be at least d.
                    if aa[pos] <= aa[i] + limit:
                        return True

            return False

        # For k >= 4, the answer cannot exceed side.
        # Also, k points on a circle of circumference C have min gap <= floor(C / k).
        lo = 0
        hi = min(side, C // k)

        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1

        return lo