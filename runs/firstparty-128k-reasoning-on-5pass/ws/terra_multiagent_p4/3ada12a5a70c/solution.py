from typing import List


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        positions = []

        # Clockwise perimeter coordinate in [0, 4 * side).
        # Corner ownership is deterministic and produces the same coordinate
        # as either incident side would.
        for x, y in points:
            if y == 0:
                positions.append(x)
            elif x == side:
                positions.append(side + y)
            elif y == side:
                positions.append(3 * side - x)
            else:
                positions.append(4 * side - y)

        positions.sort()
        n = len(positions)
        perimeter = 4 * side
        doubled = positions + [p + perimeter for p in positions]

        def feasible(d: int) -> bool:
            if d == 0:
                return True

            m = 2 * n
            nxt = [m] * m
            j = 0

            # nxt[i] = first point after i at circular/perimeter distance >= d.
            for i in range(m):
                if j < i + 1:
                    j = i + 1
                target = doubled[i] + d
                while j < m and doubled[j] < target:
                    j += 1
                nxt[i] = j

            # Fix each possible first selected point. Greedily taking the
            # earliest allowable next point leaves maximum room afterward.
            for start in range(n):
                cur = start

                for _ in range(k - 1):
                    cur = nxt[cur]
                    if cur >= start + n:
                        break
                else:
                    # Ensure the final selected point is sufficiently far
                    # from the first point across the wrap-around gap.
                    if doubled[cur] - doubled[start] <= perimeter - d:
                        return True

            return False

        # For k >= 4, the answer cannot exceed side.
        lo, hi = 0, side + 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid

        return lo