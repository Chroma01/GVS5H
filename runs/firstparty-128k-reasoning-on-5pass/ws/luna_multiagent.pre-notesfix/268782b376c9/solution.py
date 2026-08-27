from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def feasible(target: int) -> bool:
            if target == 0:
                return True

            # First move: enter index 0 and visit it once.
            moves = 1
            visits_at_current = 1

            # Process every index except the last one.
            for i in range(n - 1):
                required = (target + points[i] - 1) // points[i]
                extra = max(0, required - visits_at_current)

                # Each extra visit is obtained by an oscillation through i + 1,
                # costing 2 moves; then move to i + 1.
                moves += 2 * extra + 1
                if moves > m:
                    return False

                # The oscillations plus the final move give these visits to i + 1.
                visits_at_current = extra + 1

            # At the last index, extra visits require returning to the previous
            # index and coming back, costing 2 moves per extra visit.
            required = (target + points[-1] - 1) // points[-1]
            extra = max(0, required - visits_at_current)
            moves += 2 * extra

            return moves <= m

        low = 0
        high = min(points) * m + 1  # exclusive upper bound

        while low + 1 < high:
            mid = (low + high) // 2
            if feasible(mid):
                low = mid
            else:
                high = mid

        return low