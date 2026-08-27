from functools import lru_cache


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_up_to(x: int) -> int:
            if x <= 0:
                return 0

            digits = tuple(int(c) for c in str(x))
            n = len(digits)
            total = 0

            for target_sum in range(1, 9 * n + 1):
                @lru_cache(maxsize=None)
                def dfs(
                    pos: int,
                    digit_sum: int,
                    product_mod: int,
                    started: bool,
                    has_zero: bool,
                    tight: bool,
                ) -> int:
                    if digit_sum > target_sum:
                        return 0
                    if digit_sum + 9 * (n - pos) < target_sum:
                        return 0

                    if pos == n:
                        if digit_sum != target_sum:
                            return 0
                        return int(started and (has_zero or product_mod == 0))

                    limit = digits[pos] if tight else 9
                    result = 0

                    for d in range(limit + 1):
                        next_tight = tight and (d == digits[pos])

                        if not started:
                            if d == 0:
                                # Still leading zeroes: they do not affect
                                # either the digit sum or digit product.
                                result += dfs(
                                    pos + 1,
                                    0,
                                    1 % target_sum,
                                    False,
                                    False,
                                    next_tight,
                                )
                            else:
                                result += dfs(
                                    pos + 1,
                                    d,
                                    d % target_sum,
                                    True,
                                    False,
                                    next_tight,
                                )
                        elif has_zero:
                            # Once an actual zero occurs, the product is zero
                            # forever, so only the sum remains relevant.
                            result += dfs(
                                pos + 1,
                                digit_sum + d,
                                0,
                                True,
                                True,
                                next_tight,
                            )
                        elif d == 0:
                            result += dfs(
                                pos + 1,
                                digit_sum,
                                0,
                                True,
                                True,
                                next_tight,
                            )
                        else:
                            result += dfs(
                                pos + 1,
                                digit_sum + d,
                                (product_mod * d) % target_sum,
                                True,
                                False,
                                next_tight,
                            )

                    return result

                total += dfs(0, 0, 1 % target_sum, False, False, True)

            return total

        return count_up_to(r) - count_up_to(l - 1)