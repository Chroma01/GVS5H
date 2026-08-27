from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        if m < n:
            return 0

        minp = min(points)
        maxp = max(points)

        # The n-move sweep 0,1,...,n-1 is always possible when m >= n.
        lo = minp
        hi = min(m * minp, (m * maxp) // n) + 1
        if hi <= lo + 1:
            return lo

        NEG = -10**30
        h = [0] * n
        A = [0] * n
        B = [0] * n

        base = 2 * n - 1
        extra = m - n
        pts = points
        nn = n
        mm = m
        bb = base
        neg = NEG

        def feasible(X: int) -> bool:
            if X == 0:
                return True

            x = X - 1
            hh = h
            AA = A
            BB = B
            limit = extra
            total_h = 0

            # Suffix DP for S_t = [low_t, ..., low_{n-2}, high_{n-1}].
            # A[i] = best independent set on S_i with first vertex not chosen.
            # B[i] = best independent set on S_i with first vertex chosen.
            i = nn - 1
            hi_val = x // pts[i]
            hh[i] = hi_val
            total_h += hi_val
            if total_h > limit:
                return False
            AA[i] = 0
            BB[i] = hi_val
            a_next = 0
            b_next = hi_val

            for i in range(nn - 2, -1, -1):
                hi_val = x // pts[i]
                hh[i] = hi_val
                total_h += hi_val
                if total_h > limit:
                    return False

                w = hi_val - 1 if hi_val else 0
                b_i = w + a_next
                if a_next >= b_next:
                    a_i = a_next
                else:
                    a_i = b_next

                AA[i] = a_i
                BB[i] = b_i
                a_next = a_i
                b_next = b_i

            # Prefix DP for high weights [h_0, ..., h_{t-1}].
            # p0 = best with last vertex not chosen, p1 = best with last chosen.
            p0 = 0
            p1 = neg

            for t in range(nn - 1):
                base_cost = bb - t
                if base_cost <= mm:
                    at = AA[t]
                    bt = BB[t]
                    s_best = at if at >= bt else bt

                    val1 = p0 + s_best
                    val2 = p1 + at
                    mw = val1 if val1 >= val2 else val2

                    if base_cost + 2 * mw <= mm:
                        return True

                w = hh[t]
                old_p0 = p0
                np0 = p0 if p0 >= p1 else p1
                np1 = old_p0 + w
                p0 = np0
                p1 = np1

            # t = n - 1
            base_cost = bb - (nn - 1)
            if base_cost <= mm:
                at = AA[nn - 1]
                bt = BB[nn - 1]
                s_best = at if at >= bt else bt

                val1 = p0 + s_best
                val2 = p1 + at
                mw = val1 if val1 >= val2 else val2

                if base_cost + 2 * mw <= mm:
                    return True

            return False

        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid

        return lo