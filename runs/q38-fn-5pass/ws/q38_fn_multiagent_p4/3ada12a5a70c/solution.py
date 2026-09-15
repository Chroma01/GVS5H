from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        C = 4 * side

        # Map each boundary point to a unique perimeter coordinate in [0, C).
        coords = []
        for x, y in points:
            if y == 0:
                t = x
            elif x == side:
                t = side + y
            elif y == side:
                t = 3 * side - x
            else:
                # x == 0, left side; (0, 0) was already handled above.
                t = C - y
            coords.append(t)

        coords.sort()
        n = len(coords)
        p2 = coords + [c + C for c in coords]
        m = 2 * n

        def can(d: int) -> bool:
            if d == 0:
                return True

            # k circular gaps of at least d cannot fit in circumference C.
            if d * k > C:
                return False

            # nxt[i] = first index j > i with p2[j] >= p2[i] + d.
            nxt = [m] * (m + 1)
            arr = p2
            j = 0
            for i in range(m):
                if j <= i:
                    j = i + 1
                target = arr[i] + d
                while j < m and arr[j] < target:
                    j += 1
                nxt[i] = j

            limit = C - d
            steps = k - 1
            step_range = range(steps)

            # Try every point as the first chosen point in circular order.
            for start in range(n):
                idx = start
                max_idx = start + n  # indices [start, start+n) contain each point once
                for _ in step_range:
                    idx = nxt[idx]
                    if idx >= max_idx:
                        break
                else:
                    # Wrap-around gap from last chosen point back to start.
                    if arr[idx] <= arr[start] + limit:
                        return True

            return False

        # For k >= 4, the answer is never larger than side.
        # Also, k gaps of length d require d <= C // k.
        lo, hi = 0, min(side, C // k)

        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can(mid):
                lo = mid
            else:
                hi = mid - 1

        return lo