from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        maxP = max(points)
        base = 2 * n - 1  # = 1 + 2*(n-1); total moves = base - f + 2*W(f)

        def feasible(T: int) -> bool:
            # visits required at each index so its gameScore reaches >= T
            need = [(T + p - 1) // p for p in points]

            # Prefix MWIS over nodes 0..f-1 with weights p_i = max(0, need[i]-1).
            # PN[f] = MWIS of nodes 0..f-1 with node f-1 NOT chosen
            # PS[f] = MWIS of nodes 0..f-1 with node f-1 chosen
            PN = [0] * n
            PS = [0] * n
            PS[0] = -1  # impossible sentinel (all real weights >= 0)
            for f in range(1, n):
                w = need[f - 1] - 1
                if w < 0:
                    w = 0
                pn = PN[f - 1]
                ps = PS[f - 1]
                PN[f] = pn if pn > ps else ps
                PS[f] = pn + w

            # Suffix DP over nodes f..n-1 with weights
            # q_i = max(0, need[i]-2) for i <= n-2, and r = max(0, need[n-1]-1).
            r = need[n - 1] - 1
            if r < 0:
                r = 0
            SN = 0   # node n-1 NOT chosen
            SS = r   # node n-1 chosen

            # f = n-1 (prefix = nodes 0..n-2, suffix = node n-1)
            a = PN[n - 1] + (SN if SN > SS else SS)
            b = PS[n - 1] + SN
            W = a if a > b else b
            best = base - (n - 1) + 2 * W

            for f in range(n - 2, -1, -1):
                q = need[f] - 2
                if q < 0:
                    q = 0
                nSN = SN if SN > SS else SS   # node f NOT chosen
                nSS = q + SN                  # node f chosen -> node f+1 NOT chosen
                SN = nSN
                SS = nSS
                if f == 0:
                    W = SN if SN > SS else SS           # no prefix
                else:
                    a = PN[f] + (SN if SN > SS else SS)  # prefix last NOT chosen
                    b = PS[f] + SN                       # prefix last chosen
                    W = a if a > b else b
                c = base - f + 2 * W
                if c < best:
                    best = c
            return best <= m

        lo, hi = 0, maxP * m
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo