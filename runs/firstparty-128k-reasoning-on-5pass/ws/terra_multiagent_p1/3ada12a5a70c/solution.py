from typing import List


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        # Canonical clockwise perimeter coordinate:
        # bottom: [0, side), right: [side, 2*side),
        # top: [2*side, 3*side), left: [3*side, 4*side).
        pos = []
        for x, y in points:
            if y == 0:
                pos.append(x)
            elif x == side:
                pos.append(side + y)
            elif y == side:
                pos.append(3 * side - x)
            else:
                pos.append(4 * side - y)

        pos.sort()
        n = len(pos)
        perimeter = 4 * side

        # For k >= 4, a distance greater than side is impossible:
        # four selected points would need one point on each canonical side.
        # The four adjacent-side distances sum exactly 4*side, so they
        # cannot all be greater than side.
        #
        # Hence only d <= side needs checking. In this range, every
        # opposite-side pair is automatically at distance >= side >= d,
        # and all other relevant constraints are exactly circular
        # perimeter spacing constraints.
        doubled = pos + [x + perimeter for x in pos]

        def feasible(d: int) -> bool:
            nxt = [2 * n] * (2 * n + 1)
            j = 0

            # nxt[i] is the first perimeter point at least d ahead of i.
            for i in range(2 * n):
                if j < i + 1:
                    j = i + 1
                target = doubled[i] + d
                while j < 2 * n and doubled[j] < target:
                    j += 1
                nxt[i] = j

            # Try every point as the first selected point. Greedily taking
            # earliest possible successors is optimal for a fixed first point.
            for start in range(n):
                cur = start
                for _ in range(k - 1):
                    cur = nxt[cur]
                    if cur >= 2 * n:
                        break

                # Last-to-first wraparound perimeter gap must also be >= d.
                if cur < start + n and doubled[cur] <= doubled[start] + perimeter - d:
                    return True

            return False

        lo, hi = 0, side
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1

        return lo