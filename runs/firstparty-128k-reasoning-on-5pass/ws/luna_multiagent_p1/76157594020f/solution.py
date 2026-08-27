class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)

        def feasible(limit: int) -> bool:
            if limit == 1:
                mismatches_starting_zero = 0
                for i, ch in enumerate(s):
                    expected = '0' if i % 2 == 0 else '1'
                    if ch != expected:
                        mismatches_starting_zero += 1

                mismatches_starting_one = n - mismatches_starting_zero
                return min(mismatches_starting_zero, mismatches_starting_one) <= numOps

            inf = numOps + n + 1

            # dp0[r - 1] and dp1[r - 1] represent the minimum flips needed
            # after processing the current prefix, ending in bit 0 or 1,
            # with a final run of length r.
            dp0 = [inf] * limit
            dp1 = [inf] * limit

            first = s[0]
            dp0[0] = 0 if first == '0' else 1
            dp1[0] = 0 if first == '1' else 1

            for ch in s[1:]:
                cost0 = 0 if ch == '0' else 1
                cost1 = 0 if ch == '1' else 1

                ndp0 = [inf] * limit
                ndp1 = [inf] * limit

                # Start a run of 0 or 1 by switching from the opposite bit.
                ndp0[0] = min(dp1) + cost0
                ndp1[0] = min(dp0) + cost1

                # Extend an existing run, provided it remains within limit.
                for r in range(1, limit):
                    ndp0[r] = dp0[r - 1] + cost0
                    ndp1[r] = dp1[r - 1] + cost1

                dp0, dp1 = ndp0, ndp1

            return min(min(dp0), min(dp1)) <= numOps

        low, high = 1, n
        while low < high:
            mid = (low + high) // 2
            if feasible(mid):
                high = mid
            else:
                low = mid + 1

        return low