from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        if m < n:
            return 0

        minp = min(points)
        if m == n:
            return minp

        if n == 1:
            return points[0]

        pts = points
        nn = n
        mm = m

        def feasible(x: int, pts=pts, nn=nn, mm=mm) -> bool:
            if x == 0:
                return True

            d = [0] * nn
            total = nn
            x1 = x - 1

            for i in range(nn):
                actual = x1 // pts[i]
                if actual > mm - total:
                    return False
                total += actual
                d[i] = actual

            suf0 = [0] * (nn + 1)
            suf1 = [0] * (nn + 1)

            suf0[nn - 1] = 0
            suf1[nn - 1] = d[nn - 1]

            for i in range(nn - 2, -1, -1):
                w = d[i] - 1
                if w < 0:
                    w = 0

                a_next = suf0[i + 1]
                b_next = suf1[i + 1]

                suf0[i] = a_next if a_next >= b_next else b_next
                suf1[i] = w + a_next

            S = suf0[0] if suf0[0] >= suf1[0] else suf1[0]
            base = 2 * nn - 1
            if base <= mm and S <= (mm - base) // 2:
                return True

            p0 = 0
            p1 = -1
            base = 2 * nn - 2

            for f in range(1, nn):
                w = d[f - 1]
                new_p1 = w + p0
                new_p0 = p0 if p0 >= p1 else p1
                p0, p1 = new_p0, new_p1

                a = suf0[f]
                b = suf1[f]
                total_suf = a if a >= b else b

                opt1 = p0 + total_suf
                opt2 = p1 + a
                S = opt1 if opt1 >= opt2 else opt2

                if base <= mm and S <= (mm - base) // 2:
                    return True

                base -= 1

            return False

        lo = minp
        hi = mm * minp
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1

        return lo