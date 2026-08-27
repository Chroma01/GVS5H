from functools import lru_cache


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_up_to(x: int) -> int:
            if x <= 0:
                return 0

            digits = list(map(int, f"{x:09d}"))
            total = 0

            for target_sum in range(1, 82):
                @lru_cache(None)
                def free(pos: int, digit_sum: int,
                         product_mod: int, started: bool) -> int:
                    if digit_sum > target_sum:
                        return 0

                    remaining = 9 - pos
                    if digit_sum + 9 * remaining < target_sum:
                        return 0

                    if pos == 9:
                        return int(
                            started
                            and digit_sum == target_sum
                            and product_mod == 0
                        )

                    result = 0

                    for digit in range(10):
                        new_sum = digit_sum + digit
                        if new_sum > target_sum:
                            continue

                        if not started:
                            if digit == 0:
                                result += free(
                                    pos + 1, new_sum, 0, False
                                )
                            else:
                                result += free(
                                    pos + 1,
                                    new_sum,
                                    digit % target_sum,
                                    True,
                                )
                        else:
                            result += free(
                                pos + 1,
                                new_sum,
                                (product_mod * digit) % target_sum,
                                True,
                            )

                    return result

                result = 0
                digit_sum = 0
                product_mod = 0
                started = False

                for pos, limit in enumerate(digits):
                    for digit in range(limit):
                        new_sum = digit_sum + digit
                        if new_sum > target_sum:
                            continue

                        if not started:
                            if digit == 0:
                                result += free(
                                    pos + 1, new_sum, 0, False
                                )
                            else:
                                result += free(
                                    pos + 1,
                                    new_sum,
                                    digit % target_sum,
                                    True,
                                )
                        else:
                            result += free(
                                pos + 1,
                                new_sum,
                                (product_mod * digit) % target_sum,
                                True,
                            )

                    digit_sum += limit
                    if digit_sum > target_sum:
                        break

                    if not started:
                        if limit == 0:
                            product_mod = 0
                        else:
                            product_mod = limit % target_sum
                            started = True
                    else:
                        product_mod = (product_mod * limit) % target_sum
                else:
                    if (
                        started
                        and digit_sum == target_sum
                        and product_mod == 0
                    ):
                        result += 1

                total += result

            return total

        return count_up_to(r) - count_up_to(l - 1)