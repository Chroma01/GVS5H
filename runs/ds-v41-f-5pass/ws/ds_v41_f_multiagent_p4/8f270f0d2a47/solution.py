from functools import lru_cache


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_upto(n: int) -> int:
            if n <= 0:
                return 0

            digits = list(map(int, str(n)))
            L = len(digits)

            @lru_cache(maxsize=None)
            def dp(pos: int, started: bool, sumd: int, prod: int, tight: bool) -> int:
                if pos == L:
                    return 1 if started and sumd > 0 and prod % sumd == 0 else 0

                limit = digits[pos] if tight else 9
                total = 0

                for d in range(limit + 1):
                    ntight = tight and (d == limit)

                    if not started and d == 0:
                        # Leading zero: does not affect sum or product.
                        total += dp(pos + 1, False, 0, 1, ntight)
                    else:
                        # A real zero digit makes the whole product zero.
                        total += dp(pos + 1, True, sumd + d, prod * d, ntight)

                return total

            return dp(0, False, 0, 1, True)

        return count_upto(r) - count_upto(l - 1)