from functools import lru_cache

class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count(x: int) -> int:
            if x <= 0:
                return 0
            digits = list(map(int, str(x)))
            n = len(digits)

            @lru_cache(maxsize=None)
            def dp(pos: int, started: bool, s: int, prod: int) -> int:
                # prod == 0 means a zero digit has appeared (product is exactly 0,
                # which is divisible by any positive sum).
                if pos == n:
                    if not started:
                        return 0
                    if prod == 0:
                        return 1
                    return 1 if prod % s == 0 else 0
                total = 0
                for d in range(10):
                    if not started and d == 0:
                        total += dp(pos + 1, False, 0, 1)
                    else:
                        ns = s + d
                        nprod = 0 if (prod == 0 or d == 0) else prod * d
                        total += dp(pos + 1, True, ns, nprod)
                return total

            def solve(pos: int, tight: bool, started: bool, s: int, prod: int) -> int:
                if pos == n:
                    if not started:
                        return 0
                    if prod == 0:
                        return 1
                    return 1 if prod % s == 0 else 0
                limit = digits[pos] if tight else 9
                total = 0
                for d in range(limit + 1):
                    ntight = tight and (d == limit)
                    if not started and d == 0:
                        if ntight:
                            total += solve(pos + 1, True, False, 0, 1)
                        else:
                            total += dp(pos + 1, False, 0, 1)
                    else:
                        ns = s + d
                        nprod = 0 if (prod == 0 or d == 0) else prod * d
                        if ntight:
                            total += solve(pos + 1, True, True, ns, nprod)
                        else:
                            total += dp(pos + 1, True, ns, nprod)
                return total

            return solve(0, True, False, 0, 1)

        return count(r) - count(l - 1)