from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def check(target: int) -> bool:
            # Minimum moves to ensure index i is visited at least
            # k_i = ceil(target / points[i]) times, starting from -1.
            #
            # Greedy from right to left:
            #   carry = number of extra visits to position i already provided
            #           by excursions made on the edge (i, i+1).
            #   The first arrival at i (on the way to the end) gives 1 visit.
            #   Any further needed visits are obtained by excursions across
            #   edge (i-1, i): each excursion visits i once more, costs
            #   2 extra moves, and also gives one extra visit to i-1.
            moves = n  # moves to first reach index n-1
            carry = 0  # extra visits to i from the right side
            for i in range(n - 1, -1, -1):
                k = (target + points[i] - 1) // points[i]
                need = k - 1 - carry  # subtract first-arrival visit and carried visits
                if need > 0:
                    moves += 2 * need
                    carry = need
                else:
                    carry = 0
                if moves > m:  # early exit
                    return False
            return moves <= m

        lo, hi = 0, max(points) * m  # upper bound: put all moves on the best cell
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if check(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo