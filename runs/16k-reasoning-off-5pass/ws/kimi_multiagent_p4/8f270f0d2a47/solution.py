from functools import lru_cache


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        return self._count(r) - self._count(l - 1)

    def _count(self, x: int) -> int:
        # Count beautiful numbers in [1, x].
        if x < 1:
            return 0
        digits = list(map(int, str(x)))
        n = len(digits)
        max_sum = 9 * n
        total = 0
        for s in range(1, max_sum + 1):
            total += self._count_with_sum(digits, s)
        return total

    def _count_with_sum(self, digits, s):
        n = len(digits)

        @lru_cache(maxsize=None)
        def dp(pos, sum_so_far, prod_mod, has_zero, started, tight):
            if sum_so_far > s:
                return 0
            if pos == n:
                if not started:
                    return 0
                if sum_so_far != s:
                    return 0
                if has_zero or prod_mod % s == 0:
                    return 1
                return 0
            limit = digits[pos] if tight else 9
            total = 0
            for d in range(limit + 1):
                ntight = tight and (d == limit)
                if not started and d == 0:
                    total += dp(pos + 1, 0, prod_mod, False, False, ntight)
                else:
                    nsum = sum_so_far + d
                    if d == 0:
                        total += dp(pos + 1, nsum, prod_mod, True, True, ntight)
                    else:
                        total += dp(pos + 1, nsum, (prod_mod * d) % s, has_zero, True, ntight)
            return total

        return dp(0, 0, 1 % s, False, False, True)