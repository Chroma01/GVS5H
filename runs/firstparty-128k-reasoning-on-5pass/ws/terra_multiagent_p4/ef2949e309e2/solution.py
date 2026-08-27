from typing import List
from collections import Counter, defaultdict


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)

        def c2(x: int) -> int:
            return x * (x - 1) // 2

        def choose_small(x: int, k: int) -> int:
            if k == 0:
                return 1
            if k == 1:
                return x
            if k == 2:
                return c2(x)
            return 0

        left = defaultdict(int)
        right = Counter(nums)

        pair_left = 0
        pair_right = sum(c2(v) for v in right.values())
        cross_lr = 0
        left_sq_right = 0
        left_right_sq = 0

        ans = 0

        for i, x in enumerate(nums):
            lx = left[x]
            old_rx = right[x]

            pair_right -= old_rx - 1
            cross_lr -= lx
            left_sq_right -= lx * lx
            left_right_sq -= lx * (2 * old_rx - 1)
            right[x] -= 1

            rx = right[x]

            ln = i - lx
            rn = n - i - 1 - rx

            equal_pairs_left = pair_left - c2(lx)
            equal_pairs_right = pair_right - c2(rx)

            cross = cross_lr - lx * rx
            l2r = left_sq_right - lx * lx * rx
            lr2 = left_right_sq - lx * rx * rx

            valid = 0

            # Four additional x values: all selected values are x.
            valid += c2(lx) * c2(rx)

            # Three additional x values.
            valid += lx * ln * c2(rx)
            valid += c2(lx) * rx * rn

            # Two additional x values. Then x occurs three times and is unique mode.
            for left_x_count in range(3):
                right_x_count = 2 - left_x_count
                valid += (
                    choose_small(lx, left_x_count)
                    * choose_small(ln, 2 - left_x_count)
                    * choose_small(rx, right_x_count)
                    * choose_small(rn, 2 - right_x_count)
                )

            # One additional x value. The remaining three non-x values must be distinct.
            distinct_pairs_left = c2(ln) - equal_pairs_left
            distinct_pairs_right = c2(rn) - equal_pairs_right

            # Extra x is on the right: two left non-x values and one right non-x value.
            distinct_l2_r1 = distinct_pairs_left * rn - ln * cross + l2r

            # Extra x is on the left: one left non-x value and two right non-x values.
            distinct_l1_r2 = distinct_pairs_right * ln - rn * cross + lr2

            valid += rx * distinct_l2_r1
            valid += lx * distinct_l1_r2

            ans = (ans + valid) % MOD

            pair_left += lx
            cross_lr += rx
            left_sq_right += (2 * lx + 1) * rx
            left_right_sq += rx * rx
            left[x] += 1

        return ans