from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def feasible(target: int) -> bool:
            if target == 0:
                return True

            # First move is forced: -1 -> 0.
            moves = 1
            current_visits = 1

            # For each non-final edge, satisfy the current vertex with the
            # minimum necessary bounces, then advance to the next vertex.
            for i in range(n - 2):
                required = (target + points[i] - 1) // points[i]
                extra_bounces = max(0, required - current_visits)

                moves += 2 * extra_bounces + 1
                if moves > m:
                    return False

                # Each bounce visits i+1 once, and the final advance does too.
                current_visits = extra_bounces + 1

            penultimate_required = (
                target + points[n - 2] - 1
            ) // points[n - 2]
            last_required = (
                target + points[n - 1] - 1
            ) // points[n - 1]

            need_penultimate = max(
                0, penultimate_required - current_visits
            )

            # End at n-2: each final-edge round trip supplies one visit to
            # both n-2 and n-1.
            finish_at_penultimate = 2 * max(
                need_penultimate, last_required
            )

            # End at n-1: after q round trips, one final forward crossing
            # gives one additional visit to n-1.
            finish_at_last = 2 * max(
                need_penultimate, last_required - 1
            ) + 1

            return moves + min(
                finish_at_penultimate, finish_at_last
            ) <= m

        low = 0
        high = min(points) * m

        while low < high:
            mid = (low + high + 1) // 2
            if feasible(mid):
                low = mid
            else:
                high = mid - 1

        return low