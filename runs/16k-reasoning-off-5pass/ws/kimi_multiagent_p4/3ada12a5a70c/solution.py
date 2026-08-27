from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        P = 4 * side  # perimeter

        # Map each boundary point to its arc-length position on the perimeter,
        # walking counterclockwise starting from (0,0).
        ts = []
        for x, y in points:
            if y == 0:                      # bottom edge
                t = x
            elif x == side:                 # right edge
                t = side + y
            elif y == side:                 # top edge
                t = 2 * side + (side - x)
            else:                           # left edge (x == 0)
                t = 3 * side + (side - y)
            ts.append(t)
        ts.sort()
        n = len(ts)

        # Key facts (proof in notes):
        #   * Manhattan(p,q) <= arc(p,q) always.
        #   * If arc(p,q) < side, then Manhattan(p,q) == arc(p,q).
        #   * If p,q are on opposite edges, Manhattan(p,q) >= side.
        # Hence for any D <= side: Manhattan(p,q) >= D  <=>  arc(p,q) >= D.
        # Also, k selected points pairwise >= D apart forces k*D <= P,
        # so with k >= 4 the answer is <= P/k <= side, and the arc
        # formulation is exact over the whole search range.

        p2 = ts + [t + P for t in ts]       # duplicated ring
        N2 = 2 * n
        INF = N2

        def feasible(D: int) -> bool:
            # nxt[i] = first index j with p2[j] >= p2[i] + D (two pointers)
            nxt = [INF] * (N2 + 1)
            j = 0
            for i in range(N2):
                if j < i + 1:
                    j = i + 1
                thr = p2[i] + D
                while j < N2 and p2[j] < thr:
                    j += 1
                nxt[i] = j

            # Binary lifting: levels[b][i] = index after 2^b greedy jumps
            m = k - 1
            levels = [nxt]
            while (1 << len(levels)) <= m:
                prev = levels[-1]
                levels.append([prev[prev[i]] for i in range(N2 + 1)])

            # Try every point as the first selected one
            for i in range(n):
                limit = p2[i] + P - D       # wrap-around gap must be >= D
                cur = i
                mm = m
                b = 0
                while mm:
                    if mm & 1:
                        cur = levels[b][cur]
                    mm >>= 1
                    b += 1
                if cur < N2 and p2[cur] <= limit:
                    return True
            return False

        lo, hi = 1, P // k
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo