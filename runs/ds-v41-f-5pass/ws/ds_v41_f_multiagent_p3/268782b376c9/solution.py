from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        if m < n:
            return 0

        pts = points
        maxp = max(pts)
        # min score <= average score <= maxp*m/n
        lo = 0
        hi = maxp * m // n + 1
        NEG = -(1 << 62)

        g0 = [0] * n
        g1 = [0] * n
        base = 2 * n - 1

        def feasible(X: int) -> bool:
            Xm = X - 1
            dd = [Xm // p for p in pts]

            # suffix MWIS with "reduced" weights (max(0, d_j - 1) for j<=n-2, d_{n-1} for last)
            last = n - 1
            g1[last] = dd[last]
            g0[last] = 0
            for j in range(n - 2, -1, -1):
                dj = dd[j] - 1
                if dj < 0:
                    dj = 0
                nj = j + 1
                a = g0[nj]
                g1[j] = dj + a
                b = g1[nj]
                g0[j] = a if a > b else b

            # sweep end position e; prefix MWIS uses original weights
            f0p = 0
            f1p = NEG
            for e in range(n):
                C = g0[e]
                D = g1[e]
                m1 = f0p + (C if C > D else D)
                m2 = f1p + C
                mw = m1 if m1 > m2 else m2
                if base - e + 2 * mw <= m:
                    return True
                di = dd[e]
                nf1 = di + f0p
                nf0 = f0p if f0p > f1p else f1p
                f0p = nf0
                f1p = nf1
            return False

        while hi - lo > 1:
            mid = (lo + hi) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid
        return lo