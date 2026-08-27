from collections import Counter
from typing import List


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)

        def c2(value: int) -> int:
            return value * (value - 1) // 2

        answer = 0
        left = Counter()
        right = Counter(nums[1:])

        for i, x in enumerate(nums):
            left_x = left.get(x, 0)
            right_x = right.get(x, 0)

            left_size = i
            right_size = n - i - 1
            left_non_x = left_size - left_x
            right_non_x = right_size - right_x

            # Exactly one additional occurrence of x.
            # The other three values must be pairwise distinct and
            # different from x.
            distinct_right_pairs = c2(right_non_x)
            for value, count in right.items():
                if value != x:
                    distinct_right_pairs -= c2(count)

            collision = 0
            for value, count in right.items():
                if value != x:
                    collision += (
                        left.get(value, 0)
                        * count
                        * (right_non_x - count)
                    )

            answer += (
                left_x
                * (distinct_right_pairs * left_non_x - collision)
            )

            distinct_left_pairs = c2(left_non_x)
            for value, count in left.items():
                if value != x:
                    distinct_left_pairs -= c2(count)

            collision = 0
            for value, count in left.items():
                if value != x:
                    collision += (
                        right.get(value, 0)
                        * count
                        * (left_non_x - count)
                    )

            answer += (
                right_x
                * (distinct_left_pairs * right_non_x - collision)
            )

            # Exactly two additional occurrences of x.
            answer += (
                c2(right_x) * c2(left_non_x)
                + left_x * right_x * left_non_x * right_non_x
                + c2(left_x) * c2(right_non_x)
            )

            # At least three additional occurrences of x.
            answer += (
                c2(left_x) * right_x * right_non_x
                + left_x * c2(right_x) * left_non_x
                + c2(left_x) * c2(right_x)
            )

            left[x] += 1

            if i + 1 < n:
                next_value = nums[i + 1]
                right[next_value] -= 1
                if right[next_value] == 0:
                    del right[next_value]

        return answer % MOD