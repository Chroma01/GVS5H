from typing import List
from collections import Counter

MOD = 1_000_000_007


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        n = len(nums)

        def c2(v: int) -> int:
            return v * (v - 1) // 2

        left = Counter()
        right = Counter(nums)
        answer = 0

        for i, x in enumerate(nums):
            right[x] -= 1
            if right[x] == 0:
                del right[x]

            lx = left.get(x, 0)
            rx = right.get(x, 0)

            nl = i - lx
            nr = (n - i - 1) - rx

            # Exactly two additional copies of x:
            # the remaining two values may be equal.
            ways_two = (
                c2(lx) * c2(nr)
                + c2(rx) * c2(nl)
                + lx * rx * nl * nr
            )

            # Exactly three additional copies of x:
            # the remaining value can be any non-x value.
            ways_three = (
                c2(lx) * rx * nr
                + lx * c2(rx) * nl
            )

            # Exactly four additional copies of x.
            ways_four = c2(lx) * c2(rx)

            # Pair counts of distinct non-x values on each side.
            distinct_left_pairs = c2(nl)
            distinct_right_pairs = c2(nr)

            for value, count in left.items():
                distinct_left_pairs -= c2(count)
            for value, count in right.items():
                distinct_right_pairs -= c2(count)

            # One additional x on the left:
            # one non-x on the left and two distinct non-x values on the right.
            left_x_case = 0
            for value, count in left.items():
                if value != x:
                    rv = right.get(value, 0)
                    left_x_case += count * (
                        distinct_right_pairs - rv * (nr - rv)
                    )

            # One additional x on the right:
            # two distinct non-x values on the left and one non-x on the right.
            right_x_case = 0
            for value, count in right.items():
                if value != x:
                    lv = left.get(value, 0)
                    right_x_case += count * (
                        distinct_left_pairs - lv * (nl - lv)
                    )

            ways_one = lx * left_x_case + rx * right_x_case

            answer = (answer + ways_one + ways_two + ways_three + ways_four) % MOD

            left[x] += 1

        return answer