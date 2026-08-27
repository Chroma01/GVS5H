from functools import lru_cache


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_up_to(x: int) -> int:
            if x <= 0:
                return 0

            digits = list(map(int, str(x)))
            n = len(digits)

            # Count positive values containing an actual zero digit.
            # Their product of digits is zero, so they are always beautiful.
            @lru_cache(None)
            def count_with_zero(pos: int, started: int, has_zero: int, tight: int) -> int:
                if pos == n:
                    return int(started and has_zero)

                limit = digits[pos] if tight else 9
                ans = 0

                for d in range(limit + 1):
                    next_started = started or d != 0
                    next_has_zero = has_zero or (started and d == 0)
                    ans += count_with_zero(
                        pos + 1,
                        int(next_started),
                        int(next_has_zero),
                        int(tight and d == digits[pos]),
                    )

                return ans

            total = count_with_zero(0, 0, 0, 1)

            # Count positive zero-free values by fixing their final digit sum.
            for target_sum in range(1, 9 * n + 1):
                @lru_cache(None)
                def dp(
                    pos: int,
                    digit_sum: int,
                    product_mod: int,
                    started: int,
                    tight: int,
                ) -> int:
                    if digit_sum > target_sum:
                        return 0

                    remaining = n - pos
                    if started and digit_sum + 9 * remaining < target_sum:
                        return 0

                    if pos == n:
                        return int(
                            started
                            and digit_sum == target_sum
                            and product_mod == 0
                        )

                    limit = digits[pos] if tight else 9
                    ans = 0

                    if not started:
                        # This zero is decimal padding and must not count as a digit.
                        ans += dp(
                            pos + 1,
                            0,
                            1 % target_sum,
                            0,
                            int(tight and digits[pos] == 0),
                        )

                        for d in range(1, limit + 1):
                            if d > target_sum:
                                break
                            ans += dp(
                                pos + 1,
                                d,
                                d % target_sum,
                                1,
                                int(tight and d == digits[pos]),
                            )
                    else:
                        # Actual zero digits are excluded; they are counted separately.
                        for d in range(1, limit + 1):
                            new_sum = digit_sum + d
                            if new_sum > target_sum:
                                break
                            ans += dp(
                                pos + 1,
                                new_sum,
                                (product_mod * d) % target_sum,
                                1,
                                int(tight and d == digits[pos]),
                            )

                    return ans

                total += dp(0, 0, 1 % target_sum, 0, 1)

            return total

        return count_up_to(r) - count_up_to(l - 1)