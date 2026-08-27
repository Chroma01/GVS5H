class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        """Return the minimum possible maximum run length after at most numOps flips."""
        n = len(s)

        cost0 = [0] * n
        cost1 = [0] * n

        hi = 1
        run = 1
        for i, ch in enumerate(s):
            if ch == '0':
                cost0[i] = 0
                cost1[i] = 1
            else:
                cost0[i] = 1
                cost1[i] = 0

            if i > 0:
                if ch == s[i - 1]:
                    run += 1
                    if run > hi:
                        hi = run
                else:
                    run = 1

        if numOps == 0:
            return hi

        if numOps >= n // 2:
            return 1

        INF = 10 ** 9

        def feasible(L: int) -> bool:
            dp0 = [INF] * (L + 1)
            dp1 = [INF] * (L + 1)

            dp0[1] = cost0[0]
            dp1[1] = cost1[0]
            m0 = cost0[0]
            m1 = cost1[0]

            d0 = dp0
            d1 = dp1

            for pos in range(1, n):
                c0 = cost0[pos]
                c1 = cost1[pos]

                old_m0 = m0
                old_m1 = m1

                v0 = c0 + old_m1
                v1 = c1 + old_m0

                nm0 = v0
                nm1 = v1

                limit = L if L < pos + 1 else pos + 1

                for r in range(limit, 1, -1):
                    v = d0[r - 1] + c0
                    d0[r] = v
                    if v < nm0:
                        nm0 = v

                    v = d1[r - 1] + c1
                    d1[r] = v
                    if v < nm1:
                        nm1 = v

                d0[1] = v0
                d1[1] = v1

                m0 = nm0
                m1 = nm1

                if m0 > numOps and m1 > numOps:
                    return False

            return m0 <= numOps or m1 <= numOps

        lo = 1
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1

        return lo