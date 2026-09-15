from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        pts = points

        def feasible(x: int) -> bool:
            # Score 0 is always achievable by making no moves.
            if x == 0:
                return True

            # For x > 0, every index must be visited at least once.
            # The shortest way to visit all indices ends at n - 1 and uses n moves.
            if m < n:
                return False

            # First mandatory move: -1 -> 0.
            moves = 1

            # cur: visits already accumulated at the current index i.
            # nxt: visits already accumulated at index i + 1 from bounces at i.
            cur = 1
            nxt = 0

            for i in range(n - 1):
                need = (x + pts[i] - 1) // pts[i]

                # An index cannot be visited more times than the total number of moves.
                if need > m:
                    return False

                # If index i is short, bounce with i + 1.
                # Each bounce costs 2 moves and adds one visit to i and i + 1.
                if cur < need:
                    d = need - cur
                    moves += 2 * d
                    if moves > m:
                        return False
                    nxt += d
                    cur = need

                # At the penultimate index, we may be able to stop here
                # if the last index has already been visited enough.
                if i == n - 2:
                    need_last = (x + pts[i + 1] - 1) // pts[i + 1]
                    if need_last > m:
                        return False

                    # End at n - 2.
                    if nxt >= need_last:
                        return True

                    # Otherwise move to the last index.
                    moves += 1
                    if moves > m:
                        return False

                    cur = nxt + 1

                    # Remaining last-index visits are covered by bouncing
                    # last <-> n - 2.
                    if cur < need_last:
                        d = need_last - cur
                        moves += 2 * d
                        if moves > m:
                            return False

                    return True

                # Move right to the next index.
                moves += 1
                if moves > m:
                    return False

                cur = nxt + 1
                nxt = 0

            return True

        # No index can receive more than m visits, so the minimum score
        # cannot exceed max(points) * m.
        lo, hi = 0, max(pts) * m + 1

        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid

        return lo