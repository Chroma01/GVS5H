class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        if n == 0:
            return 0
        if n == 1:
            return 1

        max_run = 1
        cur = 1
        for i in range(1, n):
            if s[i] == s[i - 1]:
                cur += 1
                if cur > max_run:
                    max_run = cur
            else:
                cur = 1

        if max_run == 1 or numOps == 0:
            return max_run

        bits = [1 if ch == '1' else 0 for ch in s]
        INF = numOps + 1

        def can(limit: int) -> bool:
            if limit >= max_run:
                return True

            # For limit == 1, the final string must be alternating.
            if limit == 1:
                diff0 = 0
                for i, b in enumerate(bits):
                    if b != (i & 1):
                        diff0 += 1
                return min(diff0, n - diff0) <= numOps

            # dp0[r]: min flips for processed prefix ending in '0'
            #         with current run length r.
            # dp1[r]: same for ending in '1'.
            dp0 = [INF] * (limit + 1)
            dp1 = [INF] * (limit + 1)

            if bits[0] == 0:
                dp0[1] = 0
                if numOps >= 1:
                    dp1[1] = 1
            else:
                if numOps >= 1:
                    dp0[1] = 1
                dp1[1] = 0

            min0 = dp0[1]
            min1 = dp1[1]

            for i in range(1, n):
                b = bits[i]
                cost0 = 0 if b == 0 else 1
                cost1 = 1 - cost0

                ndp0 = [INF] * (limit + 1)
                ndp1 = [INF] * (limit + 1)
                new_min0 = INF
                new_min1 = INF

                # New run of 0s of length 1: previous final char must be 1.
                if min1 <= numOps:
                    v = min1 + cost0
                    if v <= numOps:
                        ndp0[1] = v
                        new_min0 = v

                # New run of 1s of length 1: previous final char must be 0.
                if min0 <= numOps:
                    v = min0 + cost1
                    if v <= numOps:
                        ndp1[1] = v
                        new_min1 = v

                # Extend existing runs by one character, if the limit allows.
                for r in range(1, limit):
                    v = dp0[r]
                    if v <= numOps:
                        nv = v + cost0
                        if nv <= numOps:
                            ndp0[r + 1] = nv
                            if nv < new_min0:
                                new_min0 = nv

                    v = dp1[r]
                    if v <= numOps:
                        nv = v + cost1
                        if nv <= numOps:
                            ndp1[r + 1] = nv
                            if nv < new_min1:
                                new_min1 = nv

                dp0, dp1 = ndp0, ndp1
                min0, min1 = new_min0, new_min1

                if min0 > numOps and min1 > numOps:
                    return False

            return min0 <= numOps or min1 <= numOps

        lo, hi = 1, max_run
        while lo < hi:
            mid = (lo + hi) // 2
            if can(mid):
                hi = mid
            else:
                lo = mid + 1

        return lo


if __name__ == "__main__":
    sol = Solution()
    assert sol.minLength("000001", 1) == 2
    assert sol.minLength("0000", 2) == 1
    assert sol.minLength("0101", 0) == 1
    assert sol.minLength("0", 0) == 1
    assert sol.minLength("0", 1) == 1
    assert sol.minLength("00", 0) == 2
    assert sol.minLength("00", 1) == 1
    assert sol.minLength("000", 1) == 1
    assert sol.minLength("0000", 1) == 2
    assert sol.minLength("000000", 1) == 3
    assert sol.minLength("000000", 2) == 2
    assert sol.minLength("000000", 3) == 1
    assert sol.minLength("111111", 1) == 3
    assert sol.minLength("001100", 0) == 2
    assert sol.minLength("001100", 1) == 2
    assert sol.minLength("001100", 2) == 2
    assert sol.minLength("001100", 3) == 1
    assert sol.minLength("000111", 0) == 3
    assert sol.minLength("000111", 1) == 3
    assert sol.minLength("000111", 2) == 1
    assert sol.minLength("0110", 1) == 2
    assert sol.minLength("0110", 2) == 1
    assert sol.minLength("000111000", 2) == 3
    assert sol.minLength("000111000", 3) == 1
    assert sol.minLength("000001", 0) == 5
    assert sol.minLength("000001", 2) == 1
    print("all tests passed")