from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        if m < n:
            return 0

        min_point = min(points)
        last = n - 1

        def feasible(score: int) -> bool:
            if score == 0:
                return True

            pts = points
            mm = m
            nn = n
            ll = last

            # a[i] = extra visits needed if index i has base visit count 1.
            a = [0] * nn
            total = 0
            for i, p in enumerate(pts):
                r = (score + p - 1) // p
                total += r
                if total > mm:
                    return False
                a[i] = r - 1

            # Suffix MWIS DP on mixed weights:
            # for i < last, weight is max(0, a[i] - 1) = max(0, r_i - 2)
            # for last, weight is a[last]
            suff0 = [0] * nn
            suff1 = [0] * nn
            s0, s1 = 0, a[ll]
            suff0[ll] = 0
            suff1[ll] = s1

            for i in range(ll - 1, -1, -1):
                w = a[i] - 1
                if w < 0:
                    w = 0
                ns0 = s0 if s0 >= s1 else s1
                ns1 = s0 + w
                s0, s1 = ns0, ns1
                suff0[i] = s0
                suff1[i] = s1

            # Endpoint t = 0: only the suffix part exists.
            mwis = suff0[0] if suff0[0] >= suff1[0] else suff1[0]
            if 2 * nn - 1 + 2 * mwis <= mm:
                return True

            # Prefix MWIS states on a[0..t-1], maintained on the fly.
            p0, p1 = 0, a[0]
            for t in range(1, nn):
                s0 = suff0[t]
                s1 = suff1[t]
                sbest = s0 if s0 >= s1 else s1

                # Prefix boundary t-1 not taken: suffix boundary t may be taken.
                mwis1 = p0 + sbest
                # Prefix boundary t-1 taken: suffix boundary t must not be taken.
                mwis2 = p1 + s0
                mwis = mwis1 if mwis1 >= mwis2 else mwis2

                if 2 * nn - 1 - t + 2 * mwis <= mm:
                    return True

                # Add vertex t to the prefix for the next endpoint.
                if t < ll:
                    np0 = p0 if p0 >= p1 else p1
                    np1 = p0 + a[t]
                    p0, p1 = np0, np1

            return False

        low = 0
        high = min_point * m + 1

        while low < high:
            mid = (low + high + 1) // 2
            if feasible(mid):
                low = mid
            else:
                high = mid - 1

        return low