from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        if n == 0:
            return 0

        # With one cell, after the first move we are at index 0 and cannot
        # move anywhere else while staying inside the array.
        if n == 1:
            return points[0] if m >= 1 else 0

        # Positive minimum requires visiting every index at least once.
        if m < n:
            return 0

        min_p = min(points)

        # If the independent-set value is at least this, then even the
        # shortest base walk (n moves) plus two moves per pair exceeds m.
        limit = (m - n) // 2 + 1
        neg = -10**30
        base_const = 2 * n - 1
        pts = points

        def feasible(x: int) -> bool:
            if x == 0:
                return True
            if m < n:
                return False
            if x <= min_p:
                return True

            lim = limit
            a = [0] * n
            c = [0] * n
            total_r = 0

            # a_i = required extra visits beyond the mandatory first visit.
            # c_i = suffix weight when the base walk returns through i:
            #       max(0, a_i - 1), except the last index keeps a_i.
            for i in range(n - 1):
                p = pts[i]
                r = (x + p - 1) // p

                # Necessary condition: total required visits cannot exceed moves.
                if total_r + r > m:
                    return False
                total_r += r

                ar = r - 1
                ac = lim if ar > lim else ar
                a[i] = ac

                if ar <= 0:
                    bc = 0
                else:
                    bc = ar - 1
                    if bc > lim:
                        bc = lim
                c[i] = bc

            p = pts[n - 1]
            r = (x + p - 1) // p
            if total_r + r > m:
                return False
            total_r += r

            ar = r - 1
            ac = lim if ar > lim else ar
            a[n - 1] = ac
            c[n - 1] = ac

            # Suffix maximum-weight independent-set DP on c.
            # suff0[i]: best from i..n-1 with i not selected.
            # suff1[i]: best from i..n-1 with i selected.
            suff0 = [0] * (n + 1)
            suff1 = [0] * (n + 1)
            suff1[n] = neg

            for i in range(n - 1, -1, -1):
                w = c[i]

                s1 = suff0[i + 1] + w
                if s1 > lim:
                    s1 = lim

                s0 = suff0[i + 1]
                if suff1[i + 1] > s0:
                    s0 = suff1[i + 1]

                suff0[i] = s0
                suff1[i] = s1

            # Sweep prefix DP on a and combine with suffix DP for every end t.
            pref0 = 0
            pref1 = neg

            for t in range(n):
                best_suf = suff0[t]
                if suff1[t] > best_suf:
                    best_suf = suff1[t]

                # If prefix last (t-1) is not selected, suffix may be best.
                val = pref0 + best_suf

                # If prefix last is selected, suffix first (t) must not be selected.
                if pref1 != neg:
                    v2 = pref1 + suff0[t]
                    if v2 > val:
                        val = v2

                if val > lim:
                    val = lim

                base = base_const - t
                if base <= m and base + 2 * val <= m:
                    return True

                # Add a[t] to the prefix for the next split point.
                if t != n - 1:
                    new_pref1 = pref0 + a[t]
                    if new_pref1 > lim:
                        new_pref1 = lim

                    new_pref0 = pref1 if pref1 > pref0 else pref0
                    pref0, pref1 = new_pref0, new_pref1

            return False

        lo = 0
        hi = min_p * m + 1

        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid

        return lo