from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def feasible(target: int) -> bool:
            if target == 0:
                return True

            # Extra visits required after the mandatory first left-to-right pass.
            d = [(target + p - 1) // p - 1 for p in points]

            # Maximum-weight independent set on prefix [0..i], using d weights.
            pref = [0] * n
            pref[0] = d[0]
            pref[1] = max(d[0], d[1])
            for i in range(2, n):
                pref[i] = max(pref[i - 1], pref[i - 2] + d[i])

            # If the final endpoint is e < n-1, vertices e..n-2 receive
            # one additional baseline visit during the return from n-1 to e.
            h = [0] * n
            for i in range(n - 1):
                h[i] = max(0, d[i] - 1)
            h[n - 1] = d[n - 1]

            # Maximum-weight independent set on suffix [i..n-1], using h weights.
            suff = [0] * (n + 2)
            suff[n - 1] = h[n - 1]
            for i in range(n - 2, -1, -1):
                suff[i] = max(suff[i + 1], h[i] + suff[i + 2])

            # Ending at n-1: n baseline moves, then two moves per extra edge pair.
            best_moves = n + 2 * pref[n - 1]

            # Consider each ending position e in [0, n-2].
            for e in range(n - 1):
                # MWIS value with e excluded.
                exclude_e = (pref[e - 1] if e >= 1 else 0) + suff[e + 1]

                # MWIS value with e included, excluding its adjacent vertices.
                include_e = h[e]
                if e >= 2:
                    include_e += pref[e - 2]
                include_e += suff[e + 2]

                extra_pairs = max(exclude_e, include_e)

                # Go from -1 to n-1, then return to e.
                moves = 1 + e + 2 * (n - 1 - e + extra_pairs)
                best_moves = min(best_moves, moves)

            return best_moves <= m

        lo, hi = 0, min(points) * m
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1

        return lo