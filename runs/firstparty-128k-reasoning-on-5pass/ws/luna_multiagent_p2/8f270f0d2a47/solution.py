from functools import lru_cache


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_up_to(bound: int) -> int:
            if bound <= 0:
                return 0

            digits = list(map(int, str(bound)))
            n = len(digits)
            total = 0

            for target_sum in range(1, 9 * n + 1):
                @lru_cache(None)
                def dp(pos: int, digit_sum: int, product_mod: int,
                       started: bool, tight: bool) -> int:
                    if digit_sum > target_sum:
                        return 0
                    if digit_sum + 9 * (n - pos) < target_sum:
                        return 0

                    if pos == n:
                        return int(
                            started
                            and digit_sum == target_sum
                            and product_mod == 0
                        )

                    limit = digits[pos] if tight else 9
                    result = 0

                    for d in range(limit + 1):
                        next_tight = tight and (d == limit if tight else False)
                        if tight:
                            next_tight = d == digits[pos]

                        if not started and d == 0:
                            result += dp(
                                pos + 1,
                                0,
                                0,
                                False,
                                next_tight
                            )
                        else:
                            if not started:
                                next_sum = d
                                next_product = d % target_sum
                            else:
                                next_sum = digit_sum + d
                                next_product = (product_mod * d) % target_sum

                            result += dp(
                                pos + 1,
                                next_sum,
                                next_product,
                                True,
                                next_tight
                            )

                    return result

                total += dp(0, 0, 0, False, True)

            return total

        return count_up_to(r) - count_up_to(l - 1)