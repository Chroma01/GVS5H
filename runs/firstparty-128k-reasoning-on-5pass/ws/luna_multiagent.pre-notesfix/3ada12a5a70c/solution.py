from bisect import bisect_left
from typing import List


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        perimeter = 4 * side
        positions = []

        # Clockwise perimeter coordinates, assigning each corner exactly once.
        for x, y in points:
            if y == 0:                  # Bottom: left to right
                pos = x
            elif x == side:             # Right: bottom to top
                pos = side + y
            elif y == side:             # Top: right to left
                pos = 3 * side - x
            else:                       # Left: top to bottom
                pos = 4 * side - y
            positions.append(pos)

        positions.sort()
        n = len(positions)
        doubled = positions + [p + perimeter for p in positions]

        def feasible(distance: int) -> bool:
            if k * distance > perimeter:
                return False

            # Fix each point as the first selected point.
            for start_idx in range(n):
                start = positions[start_idx]
                current = start
                idx = start_idx

                # Greedily select the earliest possible next point.
                for _ in range(k - 1):
                    idx = bisect_left(
                        doubled,
                        current + distance,
                        idx + 1,
                        start_idx + n
                    )

                    if idx >= start_idx + n:
                        break

                    current = doubled[idx]
                else:
                    # Ensure the final point is far enough from the start
                    # across the cyclic wraparound.
                    if current + distance <= start + perimeter:
                        return True

            return False

        # Since k >= 4, some cyclic gap among any selected k points
        # is at most side, so the answer cannot exceed side.
        lo, hi = 0, side + 1

        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid

        return lo