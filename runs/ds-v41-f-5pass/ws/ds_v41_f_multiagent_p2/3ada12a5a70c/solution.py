from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        S = side
        n = len(points)
        circ = 4 * S

        # Map each boundary point to a perimeter coordinate t in [0, 4S).
        # Direction: bottom L->R (0..S), right B->T (S..2S),
        # top R->L (2S..3S), left T->B (3S..4S). Formulas agree at corners.
        ts = []
        ap = ts.append
        for x, y in points:
            if y == 0:              # bottom: t = x
                ap(x)
            elif x == S:            # right:  t = S + y
                ap(S + y)
            elif y == S:            # top:    t = 3S - x
                ap(3 * S - x)
            else:                   # left:   t = 4S - y
                ap(4 * S - y)
        ts.sort()

        # Doubled array so circular windows become line segments.
        T = ts + [t + circ for t in ts]
        m2 = 2 * n
        km1 = k - 1
        LOG = max(1, km1.bit_length())

        def feasible(D: int) -> bool:
            # nxt[i] = first j > i with T[j] - T[i] >= D, else m2 (sentinel).
            nxt = [m2] * (m2 + 1)
            j = 1
            for i in range(m2):
                if j <= i:
                    j = i + 1
                target = T[i] + D
                while j < m2 and T[j] < target:
                    j += 1
                nxt[i] = j
            # nxt[m2] stays m2 (self-loop sentinel).

            # Binary lifting: up[b][i] = result of 2^b single jumps from i.
            up = [nxt]
            for _ in range(1, LOG):
                prev = up[-1]
                up.append([prev[prev[i]] for i in range(m2 + 1)])

            # Fix a start and jump exactly k-1 times; distinctness <=> pos < s+n,
            # wrap gap must also be >= D.
            for s in range(n):
                pos = s
                rem = km1
                b = 0
                while rem:
                    if rem & 1:
                        pos = up[b][pos]
                    rem >>= 1
                    b += 1
                if pos < s + n and T[s] + circ - T[pos] >= D:
                    return True
            return False

        # For k >= 4 no selection can have all pairwise Manhattan distances > S,
        # so the answer lies in [0, S].
        lo, hi = 0, S
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo