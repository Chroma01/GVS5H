from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def feasible(target: int) -> bool:
            # The mandatory first move is -1 -> 0.
            moves = 1
            incoming = 1  # visits already received by current index

            for i in range(n - 1):
                required = (target + points[i] - 1) // points[i]
                extra = max(0, required - incoming)

                # extra times: i -> i+1 -> i
                # then one final move: i -> i+1
                moves += 2 * extra + 1

                # At most one final move may later be removable.
                if moves > m + 1:
                    return False

                incoming = extra + 1

            required_last = (target + points[-1] - 1) // points[-1]
            extra_last = max(0, required_last - incoming)

            # Extra visits to the last position need:
            # last -> n-2 -> last
            moves += 2 * extra_last

            # If the last position already had a surplus visit before the
            # final forward crossing, omit that crossing and end at n-2.
            if extra_last == 0 and incoming > required_last:
                moves -= 1

            return moves <= m

        lo = 0
        hi = min(points) * m + 1

        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid

        return lo