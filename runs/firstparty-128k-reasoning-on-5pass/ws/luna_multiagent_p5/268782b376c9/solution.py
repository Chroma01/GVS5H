from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def feasible(target: int) -> bool:
            if target == 0:
                return True

            required = [(target + p - 1) // p for p in points]

            # Enter index 0.
            moves = 1
            visits_current = 1

            # Process all non-final boundaries greedily.
            # We must move onward, so after satisfying index i we end at i + 1.
            for i in range(n - 2):
                extra = max(0, required[i] - visits_current)
                moves += 2 * extra + 1
                if moves > m:
                    return False

                # Each back-and-forth pair, plus the final crossing, visits
                # index i + 1 exactly once.
                visits_current = extra + 1

            # Handle the final boundary separately. Let extra be the number
            # of pairs between n-2 and n-1 needed for index n-2.
            extra = max(0, required[n - 2] - visits_current)

            # End at n-2 after `t` pairs, or end at n-1 after `t` pairs
            # and one final crossing. Choose the cheaper valid endpoint.
            cost_end_previous = 2 * max(extra, required[n - 1])
            cost_end_last = 2 * max(extra, required[n - 1] - 1) + 1

            moves += min(cost_end_previous, cost_end_last)
            return moves <= m

        low, high = 0, m * max(points)

        while low < high:
            mid = (low + high + 1) // 2
            if feasible(mid):
                low = mid
            else:
                high = mid - 1

        return low