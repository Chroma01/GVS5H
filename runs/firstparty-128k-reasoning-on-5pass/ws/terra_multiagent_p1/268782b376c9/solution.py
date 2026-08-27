from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def feasible(target: int) -> bool:
            if target == 0:
                return True

            # First move: -1 -> 0.
            moves = 1
            visits_on_arrival = 1
            final_edge_bounces = 0

            for i in range(n - 1):
                required = (target + points[i] - 1) // points[i]

                # Each bounce i -> i+1 -> i supplies one additional visit
                # to i and also one visit to i+1.
                bounces = max(0, required - visits_on_arrival)
                moves += 2 * bounces + 1

                # The final forward move and all bounce forward moves visit i+1.
                visits_on_arrival = bounces + 1
                final_edge_bounces = bounces

                if moves > m + 2 * n:
                    # Early exit is safe: moves only increases afterwards.
                    return False

            required_last = (target + points[-1] - 1) // points[-1]
            remaining = max(0, required_last - visits_on_arrival)
            moves += 2 * remaining

            # If final-edge bounces already satisfy the final quota, do not
            # need the final forward step into the last position.
            if final_edge_bounces >= required_last:
                moves -= 1

            return moves <= m

        low, high = 0, min(points) * m

        while low < high:
            mid = (low + high + 1) // 2
            if feasible(mid):
                low = mid
            else:
                high = mid - 1

        return low