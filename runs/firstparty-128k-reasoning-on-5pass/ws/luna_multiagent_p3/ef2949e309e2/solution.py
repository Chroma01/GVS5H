from typing import List

MOD = 10**9 + 7


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        n = len(nums)

        compressed_map = {value: index for index, value in enumerate(set(nums))}
        arr = [compressed_map[value] for value in nums]
        distinct = len(compressed_map)

        def comb2(value: int) -> int:
            return value * (value - 1) // 2 if value >= 2 else 0

        left = [0] * distinct
        right = [0] * distinct

        for i in range(1, n):
            right[arr[i]] += 1

        left_pairs = 0
        right_pairs = sum(comb2(count) for count in right)

        # cross_left_right = sum(left[v] * C(right[v], 2))
        # cross_right_left = sum(right[v] * C(left[v], 2))
        cross_left_right = 0
        cross_right_left = 0

        answer = 0

        for middle in range(n):
            value = arr[middle]

            left_count = middle
            right_count = n - middle - 1
            left_value_count = left[value]
            right_value_count = right[value]

            # Count selections having at least two outer copies of nums[middle].
            at_least_two = 0
            for take_left_value in range(3):
                for take_right_value in range(3):
                    if take_left_value + take_right_value < 2:
                        continue

                    left_non_value = left_count - left_value_count
                    right_non_value = right_count - right_value_count

                    left_ways = (
                        (comb2(left_value_count)
                         if take_left_value == 2
                         else left_value_count
                         if take_left_value == 1
                         else 1)
                        * (
                            comb2(left_non_value)
                            if 2 - take_left_value == 2
                            else left_non_value
                            if 2 - take_left_value == 1
                            else 1
                        )
                    )

                    right_ways = (
                        (comb2(right_value_count)
                         if take_right_value == 2
                         else right_value_count
                         if take_right_value == 1
                         else 1)
                        * (
                            comb2(right_non_value)
                            if 2 - take_right_value == 2
                            else right_non_value
                            if 2 - take_right_value == 1
                            else 1
                        )
                    )

                    at_least_two += left_ways * right_ways

            left_non_value = left_count - left_value_count
            right_non_value = right_count - right_value_count

            left_pairs_without_value = (
                left_pairs - comb2(left_value_count)
            )
            right_pairs_without_value = (
                right_pairs - comb2(right_value_count)
            )

            cross_left_right_without_value = (
                cross_left_right
                - left_value_count * comb2(right_value_count)
            )
            cross_right_left_without_value = (
                cross_right_left
                - right_value_count * comb2(left_value_count)
            )

            # Three non-middle outer values must be pairwise distinct.
            one_left_two_right = (
                left_non_value * right_pairs_without_value
                - cross_left_right_without_value
            )
            two_left_one_right = (
                right_non_value * left_pairs_without_value
                - cross_right_left_without_value
            )

            # Exactly one additional copy of the middle value.
            exactly_one = (
                left_value_count * one_left_two_right
                + right_value_count * two_left_one_right
            )

            answer = (answer + at_least_two + exactly_one) % MOD

            if middle == n - 1:
                break

            # Move nums[middle] from right to left.
            current = arr[middle]
            left_count_current = left[current]
            right_count_current = right[current]

            left_pairs += left_count_current
            cross_left_right += comb2(right_count_current)
            cross_right_left += left_count_current * right_count_current
            left[current] += 1

            # Remove nums[middle + 1] from the right.
            leaving = arr[middle + 1]
            left_count_leaving = left[leaving]
            right_count_leaving = right[leaving]

            right_pairs -= comb2(right_count_leaving - 1)
            cross_left_right -= (
                left_count_leaving * (right_count_leaving - 1)
            )
            cross_right_left -= comb2(left_count_leaving)
            right[leaving] -= 1

        return answer