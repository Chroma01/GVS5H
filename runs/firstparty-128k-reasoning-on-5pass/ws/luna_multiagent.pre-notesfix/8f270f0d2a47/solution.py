from functools import lru_cache


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_up_to(n: int) -> int:
            if n <= 0:
                return 0

            digits = tuple(map(int, str(n)))
            length = len(digits)
            total = 0

            for target_sum in range(1, 9 * length + 1):
                @lru_cache(maxsize=None)
                def dp(
                    pos: int,
                    current_sum: int,
                    product_mod: int,
                    started: bool,
                    tight: bool,
                ) -> int:
                    if current_sum > target_sum:
                        return 0

                    remaining = length - pos
                    if current_sum + 9 * remaining < target_sum:
                        return 0

                    if pos == length:
                        return int(
                            started
                            and current_sum == target_sum
                            and product_mod == 0
                        )

                    limit = digits[pos] if tight else 9
                    result = 0

                    for digit in range(limit + 1):
                        next_tight = tight and digit == digits[pos]

                        if not started and digit == 0:
                            result += dp(
                                pos + 1,
                                current_sum,
                                1 % target_sum,
                                False,
                                next_tight,
                            )
                        else:
                            if started:
                                next_product = (product_mod * digit) % target_sum
                            else:
                                next_product = digit % target_sum

                            result += dp(
                                pos + 1,
                                current_sum + digit,
                                next_product,
                                True,
                                next_tight,
                            )

                    return result

                total += dp(0, 0, 1 % target_sum, False, True)

            return total

        return count_up_to(r) - count_up_to(l - 1)