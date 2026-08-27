from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def feasible(target: int) -> bool:
            if target == 0:
                return True

            required = [(target + p - 1) // p for p in points]

            # Enter index 0 on the first move.
            moves = 1
            visits = 1

            # Process every edge except the final edge.
            for i in range(n - 2):
                extra = max(0, required[i] - visits)

                # Perform extra round trips, then cross to i + 1.
                moves += 2 * extra + 1
                if moves > m:
                    return False

                # Each round trip and the final crossing visit i + 1 once.
                visits = extra + 1

            # Handle the final edge between n - 2 and n - 1.
            i = n - 2
            extra = max(0, required[i] - visits)

            # Stop at n - 1 after crossing.
            round_trips_a = max(extra, required[n - 1] - 1)
            cost_a = 2 * round_trips_a + 1

            # Stop at n - 2 without the final crossing.
            round_trips_b = max(extra, required[n - 1])
            cost_b = 2 * round_trips_b

            return moves + min(cost_a, cost_b) <= m

        low = 0
        high = (m * max(points)) // n + 1

        while low + 1 < high:
            mid = (low + high) // 2
            if feasible(mid):
                low = mid
            else:
                high = mid

        return low