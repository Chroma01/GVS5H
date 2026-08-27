from typing import List


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        perimeter = 4 * side

        def position(x: int, y: int) -> int:
            # Clockwise order: bottom, right, top, left.
            if y == 0:
                return x
            if x == side:
                return side + y
            if y == side:
                return 3 * side - x
            return 4 * side - y

        coords = sorted(position(x, y) for x, y in points)
        n = len(coords)
        doubled = coords + [x + perimeter for x in coords]
        m = 2 * n

        def can(d: int) -> bool:
            # nxt[i] is the first point at clockwise perimeter distance >= d.
            nxt = [m] * m
            r = 0

            for i in range(m):
                if r < i + 1:
                    r = i + 1

                target = doubled[i] + d
                while r < m and doubled[r] < target:
                    r += 1
                nxt[i] = r

            # For every possible first selected point, greedily choose the
            # earliest available following points. This leaves maximum room
            # for the required final-to-first cyclic gap.
            max_span = perimeter - d

            for start in range(n):
                cur = start

                for _ in range(k - 1):
                    cur = nxt[cur]
                    if cur >= m:
                        break

                if cur < m and doubled[cur] - doubled[start] <= max_span:
                    return True

            return False

        # Since k >= 4, some cyclic gap among selected points is at most side,
        # so the answer cannot exceed side.
        low, high = 1, side

        while low < high:
            mid = (low + high + 1) // 2
            if can(mid):
                low = mid
            else:
                high = mid - 1

        return low