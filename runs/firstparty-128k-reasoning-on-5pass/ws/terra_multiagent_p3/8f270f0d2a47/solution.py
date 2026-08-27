from functools import lru_cache


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_up_to(x: int) -> int:
            if x <= 0:
                return 0

            digits = list(map(int, str(x)))
            n = len(digits)

            # Every positive number containing an actual digit 0 is beautiful,
            # because its digit product is 0.
            @lru_cache(None)
            def zero_dp(pos: int, started: int, has_zero: int, tight: int) -> int:
                if pos == n:
                    return int(started and has_zero)

                limit = digits[pos] if tight else 9
                total = 0

                for d in range(limit + 1):
                    next_started = started or (d != 0)
                    # A zero is actual only after a non-leading digit appeared.
                    next_has_zero = has_zero or (started and d == 0)
                    next_tight = tight and (d == digits[pos])

                    total += zero_dp(
                        pos + 1,
                        int(next_started),
                        int(next_has_zero),
                        int(next_tight),
                    )

                return total

            answer = zero_dp(0, 0, 0, 1)

            # Count zero-free beautiful numbers by enumerating the final digit sum.
            for target_sum in range(1, 9 * n + 1):
                @lru_cache(None)
                def product_dp(
                    pos: int,
                    remaining_sum: int,
                    product_mod: int,
                    started: int,
                    tight: int,
                ) -> int:
                    slots_left = n - pos

                    if remaining_sum < 0 or remaining_sum > 9 * slots_left:
                        return 0

                    # After the number starts, all remaining digits must be nonzero.
                    if started and remaining_sum < slots_left:
                        return 0

                    if pos == n:
                        return int(started and remaining_sum == 0 and product_mod == 0)

                    limit = digits[pos] if tight else 9
                    total = 0

                    if not started:
                        # This zero is leading padding, not an actual zero digit.
                        total += product_dp(
                            pos + 1,
                            remaining_sum,
                            product_mod,
                            0,
                            int(tight and digits[pos] == 0),
                        )

                        for d in range(1, limit + 1):
                            if d > remaining_sum:
                                break
                            total += product_dp(
                                pos + 1,
                                remaining_sum - d,
                                d % target_sum,
                                1,
                                int(tight and d == digits[pos]),
                            )
                    else:
                        for d in range(1, limit + 1):
                            if d > remaining_sum:
                                break
                            total += product_dp(
                                pos + 1,
                                remaining_sum - d,
                                (product_mod * d) % target_sum,
                                1,
                                int(tight and d == digits[pos]),
                            )

                    return total

                answer += product_dp(0, target_sum, 1 % target_sum, 0, 1)

            return answer

        return count_up_to(r) - count_up_to(l - 1)