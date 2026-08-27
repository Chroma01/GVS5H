class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        def feasible(limit: int) -> bool:
            inf = 10**9

            # dp0[r]: minimum flips after the processed prefix,
            # ending in bit 0 with current run length r.
            # dp1[r]: analogous state for bit 1.
            dp0 = [inf] * (limit + 1)
            dp1 = [inf] * (limit + 1)

            dp0[1] = 0 if s[0] == '0' else 1
            dp1[1] = 0 if s[0] == '1' else 1

            for ch in s[1:]:
                cost0 = 0 if ch == '0' else 1
                cost1 = 0 if ch == '1' else 1

                best0 = min(dp0)
                best1 = min(dp1)

                next0 = [inf] * (limit + 1)
                next1 = [inf] * (limit + 1)

                # Switch the ending bit, so the new run has length 1.
                next0[1] = best1 + cost0
                next1[1] = best0 + cost1

                # Keep the same ending bit and extend its run.
                for run_length in range(2, limit + 1):
                    next0[run_length] = dp0[run_length - 1] + cost0
                    next1[run_length] = dp1[run_length - 1] + cost1

                dp0, dp1 = next0, next1

            return min(min(dp0), min(dp1)) <= numOps

        low, high = 1, n
        while low < high:
            mid = (low + high) // 2
            if feasible(mid):
                high = mid
            else:
                low = mid + 1

        return low