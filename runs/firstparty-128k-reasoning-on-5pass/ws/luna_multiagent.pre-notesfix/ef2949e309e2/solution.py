from typing import List


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)

        def c2(v: int) -> int:
            return v * (v - 1) // 2

        left = {}
        right = {}
        for value in nums:
            right[value] = right.get(value, 0) + 1

        left_pairs = 0
        right_pairs = sum(c2(freq) for freq in right.values())

        # Cross-frequency moments:
        # dot = sum(left[v] * right[v])
        # T   = sum(left[v] * right[v]^2)
        # U   = sum(left[v]^2 * right[v])
        dot = 0
        T = 0
        U = 0

        answer = 0

        for i, x in enumerate(nums):
            # Remove the current middle element from the right partition.
            old_rx = right[x]
            rx = old_rx - 1

            if rx == 0:
                del right[x]
            else:
                right[x] = rx

            lx = left.get(x, 0)

            right_pairs -= old_rx - 1
            dot -= lx
            T -= lx * (2 * old_rx - 1)
            U -= lx * lx

            left_size = i
            right_size = n - i - 1

            # Count selections with at least two additional copies of x.
            total = c2(left_size) * c2(right_size)

            non_x_left = left_size - lx
            non_x_right = right_size - rx

            no_x = c2(non_x_left) * c2(non_x_right)

            exactly_one_x = (
                lx * non_x_left * c2(non_x_right)
                + c2(non_x_left) * rx * non_x_right
            )

            at_least_two_x = total - no_x - exactly_one_x

            # Count selections with exactly one additional x.
            # The remaining three values must be pairwise distinct.
            left_pairs_without_x = left_pairs - c2(lx)
            right_pairs_without_x = right_pairs - c2(rx)

            left_distinct_pairs = (
                c2(non_x_left) - left_pairs_without_x
            )
            right_distinct_pairs = (
                c2(non_x_right) - right_pairs_without_x
            )

            dot_without_x = dot - lx * rx
            T_without_x = T - lx * rx * rx
            U_without_x = U - lx * lx * rx

            # One non-x on the left, two distinct non-x values on the right.
            ways_x_left = (
                non_x_left * right_distinct_pairs
                - (
                    non_x_right * dot_without_x
                    - T_without_x
                )
            )

            # Two distinct non-x values on the left, one non-x on the right.
            ways_x_right = (
                non_x_right * left_distinct_pairs
                - (
                    non_x_left * dot_without_x
                    - U_without_x
                )
            )

            exactly_one_additional_x = (
                lx * ways_x_left + rx * ways_x_right
            )

            answer = (
                answer
                + at_least_two_x
                + exactly_one_additional_x
            ) % MOD

            # Move the current middle element into the left partition.
            old_lx = left.get(x, 0)
            left[x] = old_lx + 1

            left_pairs += old_lx
            dot += rx
            T += rx * rx
            U += (2 * old_lx + 1) * rx

        return answer