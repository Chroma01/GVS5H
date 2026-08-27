from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def feasible(target: int) -> bool:
            # For every edge before the last one, maintain the minimum number
            # of leftward crossings needed while progressing to the right.
            need0 = (target + points[0] - 1) // points[0]
            prev_left = max(0, need0 - 1)
            total_left = prev_left

            for i in range(1, n - 1):
                need = (target + points[i] - 1) // points[i]
                cur_left = max(0, need - prev_left - 1)
                total_left += cur_left
                prev_left = cur_left

            last_need = (target + points[-1] - 1) // points[-1]

            # Finish at n - 1. There is one final net rightward crossing
            # into the last index.
            moves_end_last = n + 2 * (
                total_left + max(0, last_need - 1 - prev_left)
            )
            if moves_end_last <= m:
                return True

            # Finish at n - 2. Reaching the final index must be done through
            # complete excursions over the last edge.
            moves_end_penultimate = (n - 1) + 2 * (
                total_left + max(0, last_need - prev_left)
            )
            return moves_end_penultimate <= m

        lo = 0
        hi = m * min(points) + 1

        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid

        return lo