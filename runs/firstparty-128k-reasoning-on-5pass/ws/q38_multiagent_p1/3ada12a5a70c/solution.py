from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        C = 4 * side

        def perimeter(p: List[int]) -> int:
            x, y = p
            if y == 0:
                return x
            if x == side:
                return side + y
            if y == side:
                return 2 * side + (side - x)
            return 3 * side + (side - y)

        t = sorted(perimeter(p) for p in points)
        n = len(t)

        if k <= 1:
            return 0
        if k > n:
            return 0

        arr = t + [v + C for v in t]
        m = 2 * n
        steps = range(k - 1)

        def feasible(D: int) -> bool:
            if D == 0:
                return True
            if D * k > C:
                return False

            a = arr
            m_local = m
            nxt = [0] * m_local
            j = 0

            for i in range(m_local):
                if j < i:
                    j = i
                ai = a[i]
                while j < m_local and a[j] - ai < D:
                    j += 1
                nxt[i] = j

            nn = n
            c = C
            nxt_local = nxt

            for start in range(nn):
                idx = start
                limit = start + nn

                for _ in steps:
                    idx = nxt_local[idx]
                    if idx >= limit:
                        break
                else:
                    if a[start] + c - a[idx] >= D:
                        return True

            return False

        lo = 0
        hi = min(side, C // k) + 1

        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                lo = mid + 1
            else:
                hi = mid

        return lo - 1