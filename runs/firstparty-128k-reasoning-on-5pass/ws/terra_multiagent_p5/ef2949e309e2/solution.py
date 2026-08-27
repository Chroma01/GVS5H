from typing import List


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)

        # Coordinate compression.
        comp = {}
        arr = []
        for value in nums:
            if value not in comp:
                comp[value] = len(comp)
            arr.append(comp[value])

        m = len(comp)
        left = [0] * m
        right = [0] * m
        for value in arr:
            right[value] += 1

        def c2(value: int) -> int:
            return value * (value - 1) // 2

        # Aggregates over all compressed values y:
        # dot  = sum(left[y] * right[y])
        # lr2  = sum(left[y] * right[y]^2)
        # rl2  = sum(right[y] * left[y]^2)
        # pairL_all = sum(C(left[y], 2))
        # pairR_all = sum(C(right[y], 2))
        dot = 0
        lr2 = 0
        rl2 = 0
        pairL_all = 0
        pairR_all = sum(c2(count) for count in right)

        answer = 0

        for i, x in enumerate(arr):
            # Move nums[i] from the right structure out of consideration.
            old_right_x = right[x]
            left_x = left[x]

            pairR_all -= old_right_x - 1
            dot -= left_x
            lr2 -= left_x * (2 * old_right_x - 1)
            rl2 -= left_x * left_x
            right[x] -= 1

            right_x = right[x]
            total_left = i
            total_right = n - i - 1
            nonx_left = total_left - left_x
            nonx_right = total_right - right_x

            # Cases where at least two additional copies of x are selected.
            # Then x occurs at least 3 times, hence is necessarily the unique mode.
            many_x = 0
            for take_left_x in range(3):
                take_left_nonx = 2 - take_left_x
                if take_left_x > left_x or take_left_nonx > nonx_left:
                    continue

                ways_left = c2(left_x) if take_left_x == 2 else (
                    left_x if take_left_x == 1 else 1
                )
                ways_left *= c2(nonx_left) if take_left_nonx == 2 else (
                    nonx_left if take_left_nonx == 1 else 1
                )

                for take_right_x in range(3):
                    if take_left_x + take_right_x < 2:
                        continue

                    take_right_nonx = 2 - take_right_x
                    if take_right_x > right_x or take_right_nonx > nonx_right:
                        continue

                    ways_right = c2(right_x) if take_right_x == 2 else (
                        right_x if take_right_x == 1 else 1
                    )
                    ways_right *= c2(nonx_right) if take_right_nonx == 2 else (
                        nonx_right if take_right_nonx == 1 else 1
                    )

                    many_x += ways_left * ways_right

            # Cases with exactly one additional x.
            # The other three elements must be non-x and pairwise distinct.
            pair_left_nonx = c2(nonx_left) - (pairL_all - c2(left_x))
            pair_right_nonx = c2(nonx_right) - (pairR_all - c2(right_x))

            dot_nonx = dot - left_x * right_x
            lr2_nonx = lr2 - left_x * right_x * right_x
            rl2_nonx = rl2 - right_x * left_x * left_x

            # The extra x is selected from the left side.
            # For each chosen non-x left value y, exclude right pairs containing y.
            invalid_left_singleton = nonx_right * dot_nonx - lr2_nonx
            extra_x_left = left_x * (
                nonx_left * pair_right_nonx - invalid_left_singleton
            )

            # The extra x is selected from the right side, symmetrically.
            invalid_right_singleton = nonx_left * dot_nonx - rl2_nonx
            extra_x_right = right_x * (
                nonx_right * pair_left_nonx - invalid_right_singleton
            )

            answer = (answer + many_x + extra_x_left + extra_x_right) % MOD

            # Move nums[i] into the left structure.
            old_left_x = left[x]
            pairL_all += old_left_x
            dot += right_x
            lr2 += right_x * right_x
            rl2 += right_x * (2 * old_left_x + 1)
            left[x] += 1

        return answer