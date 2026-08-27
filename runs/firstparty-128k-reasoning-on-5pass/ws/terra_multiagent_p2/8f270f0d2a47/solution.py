from functools import lru_cache


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_up_to(x: int) -> int:
            if x <= 0:
                return 0

            digits = list(map(int, str(x)))
            n = len(digits)
            answer = 0

            # Each positive number has exactly one digit sum, so count it only
            # in the DP for that target sum.
            for target_sum in range(1, 9 * n + 1):
                @lru_cache(None)
                def dp(pos: int, current_sum: int, product_mod: int,
                       tight: bool, started: bool) -> int:
                    remaining = n - pos

                    if current_sum > target_sum:
                        return 0
                    if current_sum + 9 * remaining < target_sum:
                        return 0

                    if pos == n:
                        return int(
                            started
                            and current_sum == target_sum
                            and product_mod == 0
                        )

                    limit = digits[pos] if tight else 9
                    result = 0

                    for digit in range(limit + 1):
                        next_sum = current_sum + digit
                        if next_sum > target_sum:
                            break

                        next_started = started or digit != 0
                        if not next_started:
                            next_product = product_mod
                        else:
                            next_product = (product_mod * digit) % target_sum

                        result += dp(
                            pos + 1,
                            next_sum,
                            next_product,
                            tight and digit == limit,
                            next_started,
                        )

                    return result

                answer += dp(0, 0, 1 % target_sum, True, False)

            return answer

        return count_up_to(r) - count_up_to(l - 1)