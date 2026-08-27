import sys
from functools import lru_cache

class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        return self._count_upto(r) - self._count_upto(l - 1)

    def _count_upto(self, n: int) -> int:
        if n <= 0:
            return 0
        digits = list(map(int, str(n)))
        num_digits = len(digits)
        max_sum = 9 * num_digits
        total = 0
        # Iterate over each possible digit sum s; count numbers <= n whose
        # digit sum is exactly s and whose digit product is divisible by s.
        for s in range(1, max_sum + 1):
            total += self._count_with_sum(digits, s)
        return total

    def _count_with_sum(self, digits, s):
        @lru_cache(maxsize=None)
        def dp(pos, tight, started, sum_so_far, prod_mod):
            # pos: index into digits; tight: still equal to prefix of n
            # started: have we placed a non-leading-zero digit yet
            # sum_so_far: digit sum so far (pruned when > s)
            # prod_mod: product of digits so far modulo s (1 before started)
            if sum_so_far > s:
                return 0
            if pos == len(digits):
                if started and sum_so_far == s and prod_mod == 0:
                    return 1
                return 0
            limit = digits[pos] if tight else 9
            res = 0
            for d in range(limit + 1):
                ntight = tight and (d == limit)
                if not started and d == 0:
                    # still leading zeros: product identity stays 1 mod s
                    res += dp(pos + 1, ntight, False, 0, 1 % s)
                else:
                    res += dp(pos + 1, ntight, True,
                              sum_so_far + d, (prod_mod * d) % s)
            return res
        return dp(0, True, False, 0, 1 % s)