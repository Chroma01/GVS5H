from functools import lru_cache


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_up_to(x: int) -> int:
            if x <= 0:
                return 0

            digits = list(map(int, str(x)))
            n = len(digits)
            answer = 0

            for target_sum in range(1, 9 * n + 1):
                @lru_cache(None)
                def dp(pos: int, digit_sum: int, product_mod: int,
                       tight: bool, started: bool) -> int:
                    if digit_sum > target_sum:
                        return 0

                    remaining = n - pos
                    if digit_sum + 9 * remaining < target_sum:
                        return 0

                    if pos == n:
                        return int(
                            started
                            and digit_sum == target_sum
                            and product_mod == 0
                        )

                    limit = digits[pos] if tight else 9
                    result = 0

                    for digit in range(limit + 1):
                        next_tight = tight and (digit == digits[pos])

                        if not started and digit == 0:
                            result += dp(
                                pos + 1,
                                digit_sum,
                                product_mod,
                                next_tight,
                                False,
                            )
                        else:
                            next_sum = digit_sum + digit
                            if next_sum <= target_sum:
                                result += dp(
                                    pos + 1,
                                    next_sum,
                                    (product_mod * digit) % target_sum,
                                    next_tight,
                                    True,
                                )

                    return result

                answer += dp(0, 0, 1 % target_sum, True, False)

            return answer

        return count_up_to(r) - count_up_to(l - 1)