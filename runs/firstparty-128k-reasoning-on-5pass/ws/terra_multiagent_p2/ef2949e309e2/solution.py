from typing import List


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)

        compressed = {value: i for i, value in enumerate(set(nums))}
        a = [compressed[value] for value in nums]
        m = len(compressed)

        left = [0] * m
        right = [0] * m
        for value in a:
            right[value] += 1

        def c2(x: int) -> int:
            return x * (x - 1) // 2

        # Aggregates over all values v:
        # sum_l2 = Σ left[v]^2
        # sum_r2 = Σ right[v]^2
        # cross = Σ left[v] * right[v]
        # lr2 = Σ left[v] * right[v]^2
        # rl2 = Σ right[v] * left[v]^2
        sum_l2 = 0
        sum_r2 = sum(count * count for count in right)
        cross = 0
        lr2 = 0
        rl2 = 0

        ans = 0

        for x in a:
            # Remove current position, so right contains strictly later indices.
            lx = left[x]
            old_rx = right[x]

            sum_r2 += (old_rx - 1) * (old_rx - 1) - old_rx * old_rx
            cross -= lx
            lr2 += lx * ((old_rx - 1) * (old_rx - 1) - old_rx * old_rx)
            rl2 -= lx * lx
            right[x] -= 1
            rx = old_rx - 1

            left_total = sum(left)
            right_total = sum(right)
            ln = left_total - lx
            rn = right_total - rx

            ways = 0

            # x occurs five times.
            ways += c2(lx) * c2(rx)

            # x occurs four times.
            ways += lx * ln * c2(rx)
            ways += c2(lx) * rx * rn

            # x occurs three times.
            ways += c2(ln) * c2(rx)
            ways += lx * ln * rx * rn
            ways += c2(lx) * c2(rn)

            # x occurs exactly twice. The remaining three values must be
            # non-x and pairwise distinct.
            l_square_nonx = sum_l2 - lx * lx
            r_square_nonx = sum_r2 - rx * rx
            distinct_pairs_left = (ln * ln - l_square_nonx) // 2
            distinct_pairs_right = (rn * rn - r_square_nonx) // 2

            cross_nonx = cross - lx * rx
            lr2_nonx = lr2 - lx * rx * rx
            rl2_nonx = rl2 - rx * lx * lx

            # The second x is selected from the left.
            ways += lx * (
                ln * distinct_pairs_right
                - rn * cross_nonx
                + lr2_nonx
            )

            # The second x is selected from the right.
            ways += rx * (
                rn * distinct_pairs_left
                - ln * cross_nonx
                + rl2_nonx
            )

            ans += ways

            # Move current position into the left side.
            lx = left[x]
            rx = right[x]

            sum_l2 += (lx + 1) * (lx + 1) - lx * lx
            cross += rx
            lr2 += rx * rx
            rl2 += rx * ((lx + 1) * (lx + 1) - lx * lx)
            left[x] += 1

        return ans % MOD