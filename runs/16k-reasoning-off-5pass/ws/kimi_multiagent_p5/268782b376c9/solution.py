from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def min_moves(x: int) -> int:
            """Minimum moves so every index i is visited >= ceil(x/points[i]) times."""
            c = [(x + p - 1) // p for p in points]

            # rc[j] = rightward crossings of edge (j-1, j), j = 1..n-1.
            # Start with end position E = 0 (all e_j = 0):
            #   rc[j] >= rc[j+1]            (nested crossings)
            #   rc[j] >= c[j] - rc[j+1]     (visits to j, e_{j+1} = 0)
            #   rc[1] >= c[0] - 1           (visits to 0, e_1 = 0)
            rc = [0] * n
            rc[n - 1] = c[n - 1]
            for j in range(n - 2, 0, -1):
                rc[j] = max(rc[j + 1], c[j] - rc[j + 1])
            if n >= 2:
                rc[1] = max(rc[1], c[0] - 1)

            total_rc = sum(rc[1:])
            # Total moves for end position E: 1 + 2*sum(rc) - E.
            best = 1 + 2 * total_rc  # E = 0

            # Grow E from 1 to n-1. Flipping e_E from 0 to 1 tightens:
            #   E == 1: rc[1] >= c[0]
            #   E >= 2: rc[E-1] >= c[E-1] - rc[E] + 1
            # The increase propagates left through the max constraints.
            for E in range(1, n):
                if E == 1:
                    need = c[0]
                    j = 1
                else:
                    need = c[E - 1] - rc[E] + 1
                    j = E - 1
                # Apply tighter lower bound `need` at position j and propagate left.
                while j >= 1 and rc[j] < need:
                    total_rc += need - rc[j]
                    rc[j] = need
                    if j - 1 >= 1:
                        # constraint for rc[j-1] with e_j = 1 (since j <= E)
                        need = max(rc[j], c[j - 1] - rc[j] + 1)
                    j -= 1
                best = min(best, 1 + 2 * total_rc - E)

            return best

        lo, hi = 0, max(points) * m
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if min_moves(mid) <= m:
                lo = mid
            else:
                hi = mid - 1
        return lo