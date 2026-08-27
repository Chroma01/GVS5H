from bisect import bisect_left
from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        L = 4 * side
        ts = []
        for x, y in points:
            if y == 0:
                t = x                      # bottom edge
            elif x == side:
                t = side + y               # right edge
            elif y == side:
                t = 2 * side + (side - x)  # top edge
            else:  # x == 0
                t = 3 * side + (side - y)  # left edge
            ts.append(t)
        ts.sort()
        n = len(ts)
        t2 = ts + [t + L for t in ts]  # doubled array for circular handling

        def feasible(d: int) -> bool:
            # nxt[i] = smallest j > i with t2[j] >= t2[i] + d (two pointers, O(n))
            m = 2 * n
            nxt = [m] * m
            j = 0
            for i in range(m):
                if j < i + 1:
                    j = i + 1
                ti = t2[i] + d
                while j < m and t2[j] < ti:
                    j += 1
                nxt[i] = j
            # Greedy from every start point
            for s in range(n):
                pos = s
                ok = True
                for _ in range(k - 1):
                    pos = nxt[pos]
                    if pos >= s + n:  # wrapped past one full loop
                        ok = False
                        break
                if ok and t2[s] + L - t2[pos] >= d:  # wrap-around gap
                    return True
            return False

        lo, hi = 1, L // k  # hi <= side since k >= 4 (crucial, see NOTES)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo