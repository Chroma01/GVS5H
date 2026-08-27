from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        P = 4 * side
        # Map each boundary point to its arc-length position on the perimeter,
        # starting at (0,0) and going counterclockwise:
        # bottom edge: p = x            (covers (0,0) and (side,0))
        # right edge:  p = side + y     (covers (side,side))
        # top edge:    p = 2*side + (side - x)  (covers (0,side))
        # left edge:   p = 3*side + (side - y)
        pos = []
        for x, y in points:
            if y == 0:
                p = x
            elif x == side:
                p = side + y
            elif y == side:
                p = 2 * side + (side - x)
            else:  # x == 0
                p = 3 * side + (side - y)
            pos.append(p)
        pos.sort()
        n = len(pos)
        pos2 = pos + [p + P for p in pos]  # duplicated for circular wrap-around
        N2 = 2 * n

        def feasible(d: int) -> bool:
            # nxt[i] = smallest j > i with pos2[j] - pos2[i] >= d, else N2 (sentinel)
            nxt = [N2] * (N2 + 1)
            j = 0
            for i in range(N2):
                if j < i + 1:
                    j = i + 1
                limit = pos2[i] + d
                while j < N2 and pos2[j] < limit:
                    j += 1
                nxt[i] = j
            # Binary lifting: up[l][i] = index after 2^l greedy jumps from i
            steps = k - 1  # first point is the start itself, then k-1 jumps
            up = [nxt]
            bit = 1
            while (1 << bit) <= steps:
                prev = up[-1]
                up.append([prev[prev[i]] for i in range(N2 + 1)])
                bit += 1
            max_span = P - d  # need the wrap-around gap back to start >= d
            for i in range(n):
                cur = i
                s = steps
                b = 0
                while s:
                    if s & 1:
                        cur = up[b][cur]
                    s >>= 1
                    b += 1
                if cur < N2 and pos2[cur] - pos2[i] <= max_span:
                    return True
            return False

        # Answer never exceeds side for k >= 4 (proven in NOTES), and k gaps
        # each >= d around the circle force d <= P // k.
        lo, hi = 1, min(side, P // k)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo