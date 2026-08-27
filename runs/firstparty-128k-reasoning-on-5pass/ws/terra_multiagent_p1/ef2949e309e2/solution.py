from typing import List


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)

        compressed = {value: idx for idx, value in enumerate(set(nums))}
        arr = [compressed[value] for value in nums]
        m = len(compressed)

        left = [0] * m
        right = [0] * m
        for value in arr:
            right[value] += 1

        # Aggregates over all values v:
        # sum L[v]^2, sum R[v]^2, sum L[v]R[v],
        # sum L[v]^2R[v], sum L[v]R[v]^2.
        sum_l2 = 0
        sum_r2 = sum(count * count for count in right)
        dot = 0
        l2r = 0
        lr2 = 0

        def choose2(x: int) -> int:
            return x * (x - 1) // 2

        ans = 0

        for i, x in enumerate(arr):
            # Remove the current middle item, so right contains only
            # elements strictly after the middle.
            lx = left[x]
            old_r = right[x]
            new_r = old_r - 1

            sum_r2 += new_r * new_r - old_r * old_r
            dot -= lx
            l2r -= lx * lx
            lr2 += lx * (new_r * new_r - old_r * old_r)
            right[x] = new_r

            lsize = i
            rsize = n - i - 1
            a = left[x]
            b = right[x]

            ln = lsize - a
            rn = rsize - b

            # Aggregates restricted to values different from x.
            excl_l2 = sum_l2 - a * a
            excl_r2 = sum_r2 - b * b
            excl_dot = dot - a * b
            excl_l2r = l2r - a * a * b
            excl_lr2 = lr2 - a * b * b

            # Pairs of distinct non-x values on either side.
            pair_l_distinct = (ln * ln - excl_l2) // 2
            pair_r_distinct = (rn * rn - excl_r2) // 2

            # Exactly one extra x: x has frequency 2, hence the other
            # three selected elements must all be mutually distinct non-x values.
            valid_x_left = a * (
                pair_r_distinct * ln
                - (rn * excl_dot - excl_lr2)
            )
            valid_x_right = b * (
                pair_l_distinct * rn
                - (ln * excl_dot - excl_l2r)
            )

            # At least two extra x values: x has frequency at least 3,
            # so it is automatically the unique mode in a sequence of size 5.
            pl0 = choose2(ln)
            pl1 = a * ln
            pl2 = choose2(a)

            pr0 = choose2(rn)
            pr1 = b * rn
            pr2 = choose2(b)

            valid_x_ge_2 = (
                pl0 * pr2
                + pl1 * pr1
                + pl1 * pr2
                + pl2 * pr0
                + pl2 * pr1
                + pl2 * pr2
            )

            ans += valid_x_left + valid_x_right + valid_x_ge_2

            # Move current middle item into the left side.
            old_l = left[x]
            rx = right[x]
            new_l = old_l + 1

            sum_l2 += new_l * new_l - old_l * old_l
            dot += rx
            l2r += (new_l * new_l - old_l * old_l) * rx
            lr2 += rx * rx
            left[x] = new_l

        return ans % MOD