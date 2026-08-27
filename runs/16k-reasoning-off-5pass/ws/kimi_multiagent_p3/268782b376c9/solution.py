from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def min_moves_needed(T: int) -> int:
            """
            Minimum moves so that every gameScore[i] >= T.
            Returns a value > m if it cannot be done within m moves.

            Greedy left-to-right:
            cur = visits already guaranteed to position i by bounces done
                  for earlier positions (plus the mandatory step into i).
            If cur < need[i], bounce i <-> i+1 exactly (need[i]-cur) times
            (cost 2 each); those bounces pre-load visits onto i+1.
            Then take the mandatory step i -> i+1 (cost 1, one more visit
            to i+1).  The last index has no right neighbour, so it must
            already be satisfied by arrivals from the left.
            """
            moves = 0
            cur = 0
            for i in range(n):
                need = (T + points[i] - 1) // points[i]
                if i == n - 1:
                    if cur < need:
                        return m + 1          # impossible to fix at last index
                    break
                if cur < need:
                    extra = need - cur
                    moves += 2 * extra        # bounce i <-> i+1 `extra` times
                    cur = extra               # bounces pre-load visits to i+1
                else:
                    cur = 0
                moves += 1                    # step i -> i+1
                cur += 1                      # that step visits i+1
                if moves > m:                 # early exit
                    return m + 1
            return moves

        lo, hi = 0, 10**18
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if min_moves_needed(mid) <= m:
                lo = mid
            else:
                hi = mid - 1
        return lo