class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        if n <= 1:
            return 1

        # Doing no operations is always allowed, so the original maximum run
        # length is a valid upper bound for the answer.
        hi = 1
        run = 1
        for i in range(1, n):
            if s[i] == s[i - 1]:
                run += 1
            else:
                run = 1
            if run > hi:
                hi = run

        def feasible(limit: int) -> bool:
            # Any cost above numOps is useless; cap it to keep states small.
            INF = numOps + 1

            # dp0[length] / dp1[length]:
            # minimum flips for the processed prefix ending with 0 / 1
            # and having current identical-character run length == length.
            # Index 0 is unused.
            dp0 = [INF] * (limit + 1)
            dp1 = [INF] * (limit + 1)

            if s[0] == '0':
                dp0[1] = 0
                dp1[1] = 1
            else:
                dp0[1] = 1
                dp1[1] = 0

            best0 = min(dp0)
            best1 = min(dp1)

            for ch in s[1:]:
                target = 1 if ch == '1' else 0
                ndp0 = [INF] * (limit + 1)
                ndp1 = [INF] * (limit + 1)

                # Extend an existing run if it would not exceed limit.
                if limit > 1:
                    if target == 0:
                        for length in range(1, limit):
                            # Keep current bit 0: no extra flip.
                            v = dp0[length]
                            if v < ndp0[length + 1]:
                                ndp0[length + 1] = v

                            # Keep current bit 1: flip to 0.
                            v = dp1[length]
                            if v + 1 < ndp1[length + 1]:
                                ndp1[length + 1] = v + 1
                    else:
                        for length in range(1, limit):
                            # Keep current bit 0: flip to 1.
                            v = dp0[length]
                            if v + 1 < ndp0[length + 1]:
                                ndp0[length + 1] = v + 1

                            # Keep current bit 1: no extra flip.
                            v = dp1[length]
                            if v < ndp1[length + 1]:
                                ndp1[length + 1] = v

                # Switch to the opposite bit, resetting run length to 1.
                old_best0, old_best1 = best0, best1
                if target == 1:
                    # Previous bit 0 -> current bit 1, no flip.
                    if old_best0 < ndp1[1]:
                        ndp1[1] = old_best0

                    # Previous bit 1 -> current bit 0, one flip.
                    if old_best1 + 1 < ndp0[1]:
                        ndp0[1] = old_best1 + 1
                else:
                    # Previous bit 1 -> current bit 0, no flip.
                    if old_best1 < ndp0[1]:
                        ndp0[1] = old_best1

                    # Previous bit 0 -> current bit 1, one flip.
                    if old_best0 + 1 < ndp1[1]:
                        ndp1[1] = old_best0 + 1

                dp0, dp1 = ndp0, ndp1
                best0 = min(dp0)
                best1 = min(dp1)

                # Future characters can only add non-negative flip costs.
                if best0 > numOps and best1 > numOps:
                    return False

            return best0 <= numOps or best1 <= numOps

        lo = 1
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1

        return lo