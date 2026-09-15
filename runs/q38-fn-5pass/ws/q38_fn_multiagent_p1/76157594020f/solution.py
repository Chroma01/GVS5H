class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        if n == 0:
            return 0
        if n == 1:
            return 1

        bits = [1 if ch == '1' else 0 for ch in s]

        # Zero flips already achieve the original maximum run length.
        max_run = 1
        cur = 1
        for i in range(1, n):
            if bits[i] == bits[i - 1]:
                cur += 1
                if cur > max_run:
                    max_run = cur
            else:
                cur = 1

        if max_run == 1:
            return 1

        INF = numOps + 1

        def feasible(L: int) -> bool:
            # dp0[r]: minimum flips for the processed prefix ending with 0
            #         and current final run length r.
            # dp1[r]: same, ending with 1.
            dp0 = [INF] * (L + 1)
            dp1 = [INF] * (L + 1)

            if bits[0] == 0:
                dp0[1] = 0
                dp1[1] = 1
            else:
                dp0[1] = 1
                dp1[1] = 0

            for i in range(1, n):
                best0 = min(dp0)
                best1 = min(dp1)

                # Costs never decrease, so if every state is already too expensive,
                # no extension can become feasible.
                if best0 > numOps and best1 > numOps:
                    return False

                c0 = bits[i]       # cost to make s[i] become '0'
                c1 = 1 - c0        # cost to make s[i] become '1'

                ndp0 = [INF] * (L + 1)
                ndp1 = [INF] * (L + 1)

                # Switch to the opposite bit: current run length resets to 1.
                if best1 < INF:
                    ndp0[1] = best1 + c0
                if best0 < INF:
                    ndp1[1] = best0 + c1

                # Keep the same bit: extend the current run if it remains <= L.
                for r in range(1, L):
                    v0 = dp0[r]
                    if v0 < INF:
                        ndp0[r + 1] = v0 + c0

                    v1 = dp1[r]
                    if v1 < INF:
                        ndp1[r + 1] = v1 + c1

                dp0, dp1 = ndp0, ndp1

            return min(min(dp0), min(dp1)) <= numOps

        lo, hi = 1, max_run
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1

        return lo