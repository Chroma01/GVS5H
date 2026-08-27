from bisect import bisect_left
from typing import List


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        s = side
        P = 4 * s  # perimeter

        # Map each boundary point to its arc-length coordinate t in [0, P).
        # Order: bottom (0,0)->(s,0), right (s,0)->(s,s),
        #        top (s,s)->(0,s), left (0,s)->(0,0).
        ts = []
        for x, y in points:
            if y == 0:
                t = x
            elif x == s:
                t = s + y
            elif y == s:
                t = 2 * s + (s - x)
            else:  # x == 0
                t = 3 * s + (s - y)
            ts.append(t)
        ts.sort()
        n = len(ts)

        # Feasibility: can we pick k points with pairwise circular distance >= d?
        # Valid because for d <= side, Manhattan >= d  <=>  circular arc >= d.
        def ok(d: int) -> bool:
            # nxt[i] = first index j with ts[j] >= ts[i] + d  (always > i)
            nxt = [0] * n
            j = 0
            for i in range(n):
                if j < i + 1:
                    j = i + 1
                limit = ts[i] + d
                while j < n and ts[j] < limit:
                    j += 1
                nxt[i] = j
            # Try every point as the smallest-t selected point.
            for i in range(n - k + 1):
                cnt = 1
                cur = i
                while cnt < k:
                    cur = nxt[cur]
                    if cur >= n:
                        break
                    cnt += 1
                if cnt == k and ts[i] + P - ts[cur] >= d:
                    return True
            return False

        # Answer <= P / k (pigeonhole on arc gaps), and P/k <= side since k >= 4.
        lo, hi = 0, P // k
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if ok(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo