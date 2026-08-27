from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        """
        Returns the maximum possible value of the minimum Manhattan distance among any
        k points selected from the given points on the boundary of a square.
        The Manhattan distance between two boundary points equals the circular distance
        on the perimeter of length C = 4*side.  Thus the problem becomes:
        choose k points on a circle (perimeter C) to maximise the minimal circular
        distance between any two chosen points.
        We binary‑search the answer D and, for each D, decide if k points can be
        selected with pairwise circular distance at least D using a greedy
        construction on a duplicated (extended) array of the perimeter coordinates.
        """
        C = 4 * side                     # total perimeter length

        # ----- map each point to its position along the perimeter (clockwise) -----
        t_vals = []
        for x, y in points:
            if y == 0:                     # bottom edge
                t = x
            elif x == side:                # right edge
                t = side + y
            elif y == side:                # top edge
                t = 2 * side + (side - x)   # = 3*side - x
            else:                          # left edge (x == 0)
                t = 3 * side + (side - y)   # = 4*side - y
            t_vals.append(t)

        t_vals.sort()
        n = len(t_vals)

        # Build extended array (duplicate the points with an offset of C) to handle
        # wrap‑around.  Length is 2*n.
        t_ext = [0] * (2 * n)
        for i in range(2 * n):
            t_ext[i] = t_vals[i % n] + (i // n) * C

        # ----- binary search for the largest feasible D -----
        lo = 0
        hi = C // k                     # maximal possible D (k*D ≤ C)
        # (If C // k is 0, the answer can only be 0.)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self._feasible(t_ext, C, k, n, mid):
                lo = mid
            else:
                hi = mid - 1
        return lo

    def _feasible(self, t_ext: List[int], C: int, k: int, n: int, D: int) -> bool:
        """
        Returns True iff we can select k points from t_ext (a circular list of length
        C) such that the circular distance between any two consecutive selected
        points is at least D.  The greedy construction tries each possible start
        index and always takes the earliest possible next point.
        """
        if D == 0:
            return True
        if k * D > C:                     # necessary condition
            return False

        INF = 2 * n + 5
        # Pre‑compute for each index i the first index j > i with t_ext[j] - t_ext[i] ≥ D
        nxt = [INF] * (2 * n)
        j = 0
        for i in range(2 * n):
            if j < i + 1:
                j = i + 1
            while j < 2 * n and t_ext[j] - t_ext[i] < D:
                j += 1
            if j < 2 * n:
                nxt[i] = j
            else:
                nxt[i] = INF

        # Try every possible starting point (only the original n positions)
        for start in range(n):
            cur = start
            cnt = 1
            while cnt < k:
                nxt_cur = nxt[cur]
                if nxt_cur == INF or nxt_cur >= start + n:   # not enough room
                    break
                cur = nxt_cur
                cnt += 1
            if cnt == k:
                # Check the wrap‑around gap: distance from last point back to start
                if t_ext[cur] - t_ext[start] <= C - D:
                    return True
        return False