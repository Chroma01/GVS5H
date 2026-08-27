class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count(x: int) -> int:
            if x <= 0:
                return 0
            s = str(x)
            n = len(s)
            from functools import lru_cache

            @lru_cache(maxsize=None)
            def dp(pos: int, tight: bool, started: bool, sum_: int, prod: int, has_zero: bool) -> int:
                if pos == n:
                    if not started:
                        return 0
                    if has_zero:
                        # product is 0, divisible by any positive sum
                        return 1
                    if sum_ == 0:
                        return 0
                    return 1 if prod % sum_ == 0 else 0

                limit = int(s[pos]) if tight else 9
                total = 0
                for d in range(0, limit + 1):
                    ntight = tight and (d == limit)
                    nstarted = started or (d != 0)
                    if not nstarted:
                        # still leading zeros, nothing changes
                        total += dp(pos + 1, ntight, False, 0, 1, False)
                    else:
                        nsum = sum_ + d
                        nhas_zero = has_zero or (d == 0)
                        if nhas_zero:
                            # product becomes 0, we don't need to track it further
                            total += dp(pos + 1, ntight, True, nsum, 0, True)
                        else:
                            nprod = prod * d
                            total += dp(pos + 1, ntight, True, nsum, nprod, False)
                return total

            return dp(0, True, False, 0, 1, False)

        return count(r) - count(l - 1)