from typing import List


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 1_000_000_007
        n = len(nums)

        def choose2(value: int) -> int:
            return value * (value - 1) // 2

        left = {}
        right = {}

        for value in nums[1:]:
            right[value] = right.get(value, 0) + 1

        # Aggregates over all values:
        # l2 = sum(L[v]^2)
        # r2 = sum(R[v]^2)
        # s  = sum(L[v] * R[v])
        # u  = sum(L[v] * R[v]^2)
        # w  = sum(R[v] * L[v]^2)
        l2 = 0
        r2 = sum(count * count for count in right.values())
        s = 0
        u = 0
        w = 0

        answer = 0

        for i, x in enumerate(nums):
            lx = left.get(x, 0)
            rx = right.get(x, 0)

            left_non_x = i - lx
            right_non_x = n - i - 1 - rx

            # The middle value is the unique mode when it occurs at least
            # three times, so at least two selected side values equal x.
            at_least_three = 0

            for selected_left_x in range(3):
                selected_left_non_x = 2 - selected_left_x

                left_ways = (
                    1
                    if selected_left_x == 0
                    else lx
                    if selected_left_x == 1
                    else choose2(lx)
                )
                left_ways *= (
                    1
                    if selected_left_non_x == 0
                    else left_non_x
                    if selected_left_non_x == 1
                    else choose2(left_non_x)
                )

                for selected_right_x in range(3):
                    selected_right_non_x = 2 - selected_right_x

                    if selected_left_x + selected_right_x < 2:
                        continue

                    right_ways = (
                        1
                        if selected_right_x == 0
                        else rx
                        if selected_right_x == 1
                        else choose2(rx)
                    )
                    right_ways *= (
                        1
                        if selected_right_non_x == 0
                        else right_non_x
                        if selected_right_non_x == 1
                        else choose2(right_non_x)
                    )

                    at_least_three += left_ways * right_ways

            # Remove x from the aggregate sums.
            cross = s - lx * rx
            non_x_left_sq = l2 - lx * lx
            non_x_right_sq = r2 - rx * rx
            left_right_sq = u - lx * rx * rx
            right_left_sq = w - rx * lx * lx

            # Exactly one additional x is chosen on the left. The three
            # non-x values must all be distinct.
            one_x_left = (
                left_non_x * choose2(right_non_x)
                - left_non_x * ((non_x_right_sq - right_non_x) // 2)
                - right_non_x * cross
                + left_right_sq
            )

            # Symmetric case: exactly one additional x on the right.
            one_x_right = (
                right_non_x * choose2(left_non_x)
                - right_non_x * ((non_x_left_sq - left_non_x) // 2)
                - left_non_x * cross
                + right_left_sq
            )

            total = (
                at_least_three
                + lx * one_x_left
                + rx * one_x_right
            )
            answer = (answer + total) % MOD

            if i == n - 1:
                break

            # Move nums[i + 1] from the right side to the left-side gap.
            y = nums[i + 1]
            ly = left.get(y, 0)
            ry = right[y]

            r2 += (ry - 1) ** 2 - ry ** 2
            s -= ly
            u += ly * ((ry - 1) ** 2 - ry ** 2)
            w -= ly * ly

            if ry == 1:
                del right[y]
            else:
                right[y] = ry - 1

            # Move nums[i] into the left side.
            lx_current = left.get(x, 0)
            rx_current = right.get(x, 0)
            left_delta = (lx_current + 1) ** 2 - lx_current ** 2

            l2 += left_delta
            s += rx_current
            u += rx_current * rx_current
            w += left_delta * rx_current
            left[x] = lx_current + 1

        return answer