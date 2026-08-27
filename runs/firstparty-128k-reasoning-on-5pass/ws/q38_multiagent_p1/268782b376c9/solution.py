from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        if m < n:
            return 0

        minp = min(points)
        if m == n:
            return minp

        maxp = max(points)
        cap = m // 2 + 1
        cap1 = cap + 1
        base = 2 * n - 1

        L = [0] * n
        best = [0] * (n + 2)
        fwd = range(n)
        rev = range(n - 2, -1, -1)

        def feasible(
            x: int,
            pts=points,
            n=n,
            m=m,
            cap=cap,
            cap1=cap1,
            base=base,
            minp=minp,
            L=L,
            best=best,
            fwd=fwd,
            rev=rev,
        ) -> bool:
            if x <= minp:
                return True

            total = 0
            for i, p in enumerate(pts):
                r = (x + p - 1) // p
                total += r
                if total > m:
                    return False

                li = r - 1
                if li > cap1:
                    li = cap1
                L[i] = li

            best[n] = 0
            best[n + 1] = 0

            b = L[n - 1]
            if b > cap:
                b = cap
            best[n - 1] = b

            for i in rev:
                w = L[i] - 1
                if w < 0:
                    w = 0

                val = w + best[i + 2]
                b = best[i + 1]
                if val > b:
                    b = val

                if b > cap:
                    b = cap
                best[i] = b

            pref0 = 0
            pref1 = -1
            length = base

            for t in fwd:
                pval = pref0 + best[t]
                if pref1 >= 0:
                    p2 = pref1 + best[t + 1]
                    if p2 > pval:
                        pval = p2

                if pval > cap:
                    pval = cap

                if length + (pval << 1) <= m:
                    return True

                old0 = pref0
                old1 = pref1
                if old1 > old0:
                    pref0 = old1

                pref1 = old0 + L[t]
                if pref1 > cap:
                    pref1 = cap

                length -= 1

            return False

        lo = minp
        hi = min(m * minp, (m * maxp) // n) + 1

        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid

        return lo