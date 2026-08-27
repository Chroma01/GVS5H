from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def feasible(target: int) -> bool:
            if target == 0:
                return True

            moves = 1  # First move: -1 -> 0
            incoming = 1  # Visits already accumulated at index 0

            # Process positions before the last two.
            for i in range(n - 2):
                required = (target + points[i] - 1) // points[i]
                extra = max(0, required - incoming)

                # Each extra visit is obtained by a round trip to the right.
                moves += 2 * extra + 1
                if moves > m:
                    return False

                # Number of visits delivered to the next position.
                incoming = extra + 1

            # Process the penultimate position. We may stop there, so the
            # final transition is not automatically required.
            penultimate_required = (
                target + points[n - 2] - 1
            ) // points[n - 2]
            extra = max(0, penultimate_required - incoming)
            moves += 2 * extra

            if moves > m:
                return False

            # The extra round trips above visit the last position `extra`
            # times. If more visits are needed, enter it once and use
            # round trips back to the penultimate position.
            last_required = (target + points[n - 1] - 1) // points[n - 1]
            if last_required > extra:
                moves += 2 * (last_required - extra) - 1

            return moves <= m

        low = 0
        high = max(points) * ((m + 1) // 2)

        while low < high:
            mid = (low + high + 1) // 2
            if feasible(mid):
                low = mid
            else:
                high = mid - 1

        return low