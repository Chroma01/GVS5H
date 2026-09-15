from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        s = side
        C = 4 * s

        # Map each boundary point to its clockwise perimeter coordinate.
        # The case order assigns each corner to exactly one side, so coordinates are unique.
        coords = []
        for x, y in points:
            if y == 0:
                # bottom side: (0, 0) -> (s, 0)
                coords.append(x)
            elif x == s:
                # right side: (s, 0) -> (s, s)
                coords.append(s + y)
            elif y == s:
                # top side: (s, s) -> (0, s)
                coords.append(2 * s + (s - x))
            else:
                # left side: (0, s) -> (0, 0)
                coords.append(3 * s + (s - y))

        coords.sort()
        n = len(coords)

        # Constraints guarantee 4 <= k <= n, but these guards are harmless.
        if k <= 1 or k > n:
            return 0

        # Duplicate coordinates to handle circular wrap-around.
        arr = coords + [t + C for t in coords]
        m = 2 * n
        steps = k - 1

        def can(d: int) -> bool:
            if d == 0:
                return True

            # Necessary condition for k circular gaps of at least d.
            if k * d > C:
                return False

            # nxt[i] = first index j > i with arr[j] >= arr[i] + d.
            nxt = [m] * m
            j = 0
            a = arr

            for i in range(m):
                if j <= i:
                    j = i + 1
                target = a[i] + d
                while j < m and a[j] < target:
                    j += 1
                nxt[i] = j

            # Try every original point as the first selected point.
            for i in range(n):
                pos = i
                limit = a[i] + C - d

                for _ in range(steps):
                    pos = nxt[pos]
                    if pos >= m or a[pos] > limit:
                        break
                else:
                    return True

            return False

        # The answer is at most side. Also, k circular gaps sum to 4*side.
        lo = 0
        hi = min(s, C // k)

        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can(mid):
                lo = mid
            else:
                hi = mid - 1

        return lo