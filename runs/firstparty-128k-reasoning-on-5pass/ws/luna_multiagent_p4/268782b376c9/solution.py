from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def feasible(target: int) -> bool:
            if target == 0:
                return True

            moves = 1
            visits = 1

            for i in range(n - 2):
                required = (target + points[i] - 1) // points[i]
                extra = max(0, required - visits)

                moves += 2 * extra + 1
                if moves > m:
                    return False

                visits = extra + 1

            required_second_last = (
                target + points[n - 2] - 1
            ) // points[n - 2]
            required_last = (
                target + points[n - 1] - 1
            ) // points[n - 1]

            round_trips = max(
                0,
                required_second_last - visits,
                required_last - 1,
            )
            moves += 2 * round_trips

            if round_trips < required_last:
                moves += 1

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