from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        s = side
        P = 4 * s

        def perimeter(x: int, y: int) -> int:
            # Clockwise coordinate starting at (0,0):
            # bottom: t = x, right: t = s + y,
            # top: t = 3s - x, left: t = 4s - y.
            if y == 0:
                return x
            if x == s:
                return s + y
            if y == s:
                return 3 * s - x
            return 4 * s - y

        t = sorted(perimeter(x, y) for x, y in points)
        n = len(t)
        t2 = t + [v + P for v in t]

        def feasible(d: int) -> bool:
            if d == 0:
                return True

            n2 = 2 * n
            nxt = [n2] * n2

            # nxt[i] = smallest j > i with t2[j] >= t2[i] + d
            j = 0
            for i in range(n2):
                if j <= i:
                    j = i + 1
                target = t2[i] + d
                while j < n2 and t2[j] < target:
                    j += 1
                nxt[i] = j

            # Try every point as the first selected point.
            for i in range(n):
                cur = i
                for _ in range(k - 1):
                    cur = nxt[cur]
                    if cur == n2:
                        break
                else:
                    # Need the wrap-around gap to be at least d.
                    if t2[cur] - t2[i] <= P - d:
                        return True
            return False

        lo, hi = 0, P // k
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo