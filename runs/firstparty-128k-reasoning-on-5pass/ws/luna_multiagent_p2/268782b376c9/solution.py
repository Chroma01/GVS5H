from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def feasible(target: int) -> bool:
            if target == 0:
                return True

            # The first move, from -1 to 0, is forced.
            moves = 1
            visits_current = 1

            # Process indices before the final two.
            for i in range(n - 2):
                required = (target + points[i] - 1) // points[i]

                if visits_current < required:
                    extra = required - visits_current
                    # Each extra visit uses a round trip through i + 1,
                    # followed by one move forward.
                    moves += 2 * extra + 1
                    visits_current = extra + 1
                else:
                    moves += 1
                    visits_current = 1

                if moves > m:
                    return False

            # Handle indices n - 2 and n - 1 together.
            required_current = (
                target + points[n - 2] - 1
            ) // points[n - 2]
            extra = max(0, required_current - visits_current)

            required_last = (target + points[n - 1] - 1) // points[n - 1]

            # Each excursion from n - 2 to n - 1 and back visits the
            # final index once. We may stop at n - 2 if that suffices.
            if extra >= required_last:
                moves += 2 * extra
            else:
                # The final forward move supplies one additional visit
                # to the last index; further visits require bounces.
                remaining = required_last - extra - 1
                moves += 2 * extra + 1 + 2 * max(0, remaining)

            return moves <= m

        low = 0
        high = max(points) * m + 1

        while low + 1 < high:
            mid = (low + high) // 2
            if feasible(mid):
                low = mid
            else:
                high = mid

        return low