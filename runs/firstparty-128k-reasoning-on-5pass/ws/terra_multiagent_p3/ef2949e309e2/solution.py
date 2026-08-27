from typing import List


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)

        value_id = {value: idx for idx, value in enumerate(set(nums))}
        a = [value_id[value] for value in nums]
        m = len(value_id)

        left = [0] * m
        right = [0] * m
        for value in a:
            right[value] += 1

        def choose2(count: int) -> int:
            return count * (count - 1) // 2

        answer = 0

        for i, x in enumerate(a):
            right[x] -= 1

            lx = left[x]
            rx = right[x]
            left_total = i
            right_total = n - i - 1
            left_non_x = left_total - lx
            right_non_x = right_total - rx

            # The middle value occurs at least three times in the selected
            # subsequence, so it is automatically the unique mode.
            at_least_two_extra = 0
            for take_left_x in range(3):
                take_left_other = 2 - take_left_x
                if take_left_x > lx or take_left_other > left_non_x:
                    continue

                left_ways = (
                    (1 if take_left_x == 0 else lx if take_left_x == 1 else choose2(lx))
                    * (
                        1
                        if take_left_other == 0
                        else left_non_x
                        if take_left_other == 1
                        else choose2(left_non_x)
                    )
                )

                for take_right_x in range(3):
                    if take_left_x + take_right_x < 2:
                        continue

                    take_right_other = 2 - take_right_x
                    if take_right_x > rx or take_right_other > right_non_x:
                        continue

                    right_ways = (
                        (1 if take_right_x == 0 else rx if take_right_x == 1 else choose2(rx))
                        * (
                            1
                            if take_right_other == 0
                            else right_non_x
                            if take_right_other == 1
                            else choose2(right_non_x)
                        )
                    )
                    at_least_two_extra += left_ways * right_ways

            # If exactly one extra middle value is selected, the other three
            # values must be non-x and pairwise distinct.
            equal_left_pairs = 0
            equal_right_pairs = 0
            forbidden_right_pairs = 0
            forbidden_left_pairs = 0

            for y in range(m):
                if y == x:
                    continue

                ly = left[y]
                ry = right[y]

                equal_left_pairs += choose2(ly)
                equal_right_pairs += choose2(ry)

                # A distinct right pair containing y has one y and one
                # non-x, non-y element.
                forbidden_right_pairs += ly * ry * (right_non_x - ry)
                forbidden_left_pairs += ry * ly * (left_non_x - ly)

            distinct_left_pairs = choose2(left_non_x) - equal_left_pairs
            distinct_right_pairs = choose2(right_non_x) - equal_right_pairs

            one_extra_on_left = lx * (
                left_non_x * distinct_right_pairs - forbidden_right_pairs
            )
            one_extra_on_right = rx * (
                right_non_x * distinct_left_pairs - forbidden_left_pairs
            )

            answer += at_least_two_extra + one_extra_on_left + one_extra_on_right
            left[x] += 1

        return answer % MOD