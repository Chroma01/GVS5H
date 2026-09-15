from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        # Not needed by the official constraints (n >= 2), but keeps the code safe.
        if n == 1:
            return points[0] if m >= 1 else 0

        # For any positive answer, every index must be visited at least once.
        if m < n:
            return 0

        min_p = min(points)
        max_p = max(points)

        # Safe upper bounds:
        # 1) The minimum-point index can be visited at most m - (n - 1) times.
        # 2) Total score <= max(points) * m, so minimum score <= average score.
        hi = min(min_p * (m - n + 1), (max_p * m) // n)
        lo = 0
        if hi == 0:
            return 0

        # Reusable arrays for the O(n) feasibility check.
        B = [0] * (n - 1)       # weights r_i - 2, clipped, for i = 0..n-2
        pref0 = [0] * (n - 1)   # prefix DP on A_i = r_i - 1, last not chosen
        pref1 = [0] * (n - 1)   # prefix DP on A_i = r_i - 1, last chosen
        suff0 = [0] * n         # suffix DP on B_i + last C, first not chosen
        suff1 = [0] * n         # suffix DP on B_i + last C, first chosen

        pts = points
        mm = m
        nn = n
        base0 = 2 * nn - 1      # base moves when ending at t = 0

        def can(x: int) -> bool:
            if x <= 0:
                return True

            total = 0

            # Index 0: prefix starts here, and B[0] is needed for suffixes.
            p = pts[0]
            r = (x + p - 1) // p
            total += r
            if total > mm:
                return False

            b = r - 2
            if b < 0:
                b = 0
            B[0] = b
            pref0[0] = 0
            pref1[0] = r - 1

            # Indices 1 .. n-2.
            for i in range(1, nn - 1):
                p = pts[i]
                r = (x + p - 1) // p
                total += r
                if total > mm:
                    return False

                b = r - 2
                if b < 0:
                    b = 0
                B[i] = b

                prev0 = pref0[i - 1]
                prev1 = pref1[i - 1]
                pref0[i] = prev0 if prev0 >= prev1 else prev1
                pref1[i] = prev0 + (r - 1)

            # Last index: its weight is always C = max(0, r_last - 1).
            p = pts[-1]
            r = (x + p - 1) // p
            total += r
            if total > mm:
                return False

            c = r - 1
            if c < 0:
                c = 0

            # Suffix DP for weights B[t], B[t+1], ..., B[n-2], C.
            suff0[nn - 1] = 0
            suff1[nn - 1] = c
            for i in range(nn - 2, -1, -1):
                s0 = suff0[i + 1]
                s1 = suff1[i + 1]
                suff1[i] = s0 + B[i]
                suff0[i] = s0 if s0 >= s1 else s1

            # Try ending positions t = n-1 down to 1.
            for t in range(nn - 1, 0, -1):
                p0 = pref0[t - 1]
                p1 = pref1[t - 1]
                s0 = suff0[t]
                s1 = suff1[t]

                ms = s0 if s0 >= s1 else s1
                v1 = p0 + ms
                v2 = p1 + s0
                val = v1 if v1 >= v2 else v2

                if (base0 - t) + 2 * val <= mm:
                    return True

            # Ending position t = 0: only the suffix part exists.
            val = suff0[0] if suff0[0] >= suff1[0] else suff1[0]
            if base0 + 2 * val <= mm:
                return True

            return False

        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can(mid):
                lo = mid
            else:
                hi = mid - 1

        return lo