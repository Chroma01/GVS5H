from typing import List


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        s = side
        C = 4 * s

        # Map every boundary point to a perimeter coordinate in [0, 4s).
        # Orientation: (0,0) -> bottom -> (s,0) -> right -> (s,s) ->
        # top -> (0,s) -> left -> (0,0).
        p = []
        for x, y in points:
            if y == 0:
                p.append(x)
            elif x == s:
                p.append(s + y)
            elif y == s:
                p.append(3 * s - x)
            else:
                # x == 0
                p.append(4 * s - y)

        p.sort()
        n = len(p)
        p2 = p + [v + C for v in p]
        m = 2 * n

        def feasible(D: int) -> bool:
            if D == 0:
                return True

            # nxt[i] = first index j with p2[j] >= p2[i] + D.
            nxt = [0] * m
            j = 0
            pp = p2
            mm = m
            for i in range(mm):
                if j < i + 1:
                    j = i + 1
                target = pp[i] + D
                while j < mm and pp[j] < target:
                    j += 1
                nxt[i] = j

            # Try each point as the first selected point after cutting the circle.
            for i in range(n):
                # The last selected point must leave at least D around the wrap.
                limit = pp[i] + C - D
                cur = i
                cnt = 1

                for _ in range(k - 1):
                    cur = nxt[cur]
                    if cur >= mm or pp[cur] > limit:
                        break
                    cnt += 1
                    if cnt >= k:
                        return True

            return False

        # For k >= 4, the answer is at most side.
        lo, hi = 0, s
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1

        return lo