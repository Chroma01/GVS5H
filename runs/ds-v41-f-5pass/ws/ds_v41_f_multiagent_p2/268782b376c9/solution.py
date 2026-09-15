from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        # Must reach index n-1 so every index gets >= 1 visit; needs at least n moves.
        if m < n:
            return 0

        min_p = min(points)
        NEG = -(1 << 60)

        def feasible(x: int) -> bool:
            if x <= 0:
                return True

            # A[i] = extra visits needed if index i gets 1 visit in the base walk.
            # B[i] = extra visits needed if index i gets 2 visits in the base walk.
            A = [0] * n
            B = [0] * n
            for i in range(n):
                p = points[i]
                r = -(-x // p)            # ceil(x / p)
                if r > m:                 # impossible: total moves = total visits <= m
                    return False
                if r > 1:
                    A[i] = r - 1
                if r > 2:
                    B[i] = r - 2
            B[n - 1] = A[n - 1]           # index n-1 is visited once in the base walk
            W = B

            # Suffix DP over W: MWIS of W[i..n-1] with i NOT chosen (R0) / chosen (R1).
            R0 = [0] * (n + 1)
            R1 = [0] * (n + 1)
            R1[n] = NEG
            for i in range(n - 1, -1, -1):
                r0 = R0[i + 1]
                r1 = R1[i + 1]
                R0[i] = r0 if r0 > r1 else r1
                R1[i] = W[i] + r0

            # Prefix DP over A: MWIS of A[0..f-1] with f-1 NOT chosen (P0) / chosen (P1).
            P0 = [0] * (n + 1)
            P1 = [0] * (n + 1)
            P1[0] = NEG
            for f in range(1, n + 1):
                p0 = P0[f - 1]
                p1 = P1[f - 1]
                P0[f] = p0 if p0 > p1 else p1
                P1[f] = p0 + A[f - 1]

            best = 1 << 62
            for f in range(n):
                if f == 0:
                    mwis = R0[0] if R0[0] > R1[0] else R1[0]
                else:
                    suff = R0[f] if R0[f] > R1[f] else R1[f]
                    c1 = P0[f] + suff      # A[f-1] not chosen -> W[f] free
                    c2 = P1[f] + R0[f]     # A[f-1] chosen     -> W[f] forbidden
                    mwis = c1 if c1 > c2 else c2
                moves = 2 * n - 1 - f + 2 * mwis
                if moves < best:
                    best = moves

            return best <= m

        lo, hi = 0, min_p * m
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo