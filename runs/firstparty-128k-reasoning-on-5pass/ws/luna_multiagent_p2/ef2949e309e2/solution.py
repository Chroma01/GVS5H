from typing import List

MOD = 10**9 + 7


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        n = len(nums)

        left = {}
        right = {}
        for value in nums[1:]:
            right[value] = right.get(value, 0) + 1

        left_size = 0
        right_size = n - 1

        left_c2 = 0
        right_c2 = sum(c * (c - 1) // 2 for c in right.values())

        # For every value v:
        # a = count of v on the left
        # b = count of v on the right
        #
        # q    = sum(a*b)
        # ab2  = sum(a*b*b)
        # a2b  = sum(a*a*b)
        q = 0
        ab2 = 0
        a2b = 0

        def change(value: int, new_a: int, new_b: int) -> None:
            nonlocal left_c2, right_c2, q, ab2, a2b

            old_a = left.get(value, 0)
            old_b = right.get(value, 0)

            left_c2 -= old_a * (old_a - 1) // 2
            right_c2 -= old_b * (old_b - 1) // 2
            q -= old_a * old_b
            ab2 -= old_a * old_b * old_b
            a2b -= old_a * old_a * old_b

            left_c2 += new_a * (new_a - 1) // 2
            right_c2 += new_b * (new_b - 1) // 2
            q += new_a * new_b
            ab2 += new_a * new_b * new_b
            a2b += new_a * new_a * new_b

            if new_a:
                left[value] = new_a
            else:
                left.pop(value, None)

            if new_b:
                right[value] = new_b
            else:
                right.pop(value, None)

        answer = 0

        for j, x in enumerate(nums):
            if j > 0:
                a = left.get(x, 0)
                b = right.get(x, 0)
                change(x, a, b - 1)
                right_size -= 1

            lx = left.get(x, 0)
            rx = right.get(x, 0)

            # Counts of non-x elements on each side.
            A = left_size - lx
            B = right_size - rx

            # Pairs of distinct-valued non-x elements on each side.
            DA = left_c2 - lx * (lx - 1) // 2
            DB = right_c2 - rx * (rx - 1) // 2

            # Cross-side aggregates excluding x.
            qx = q - lx * rx
            ab2x = ab2 - lx * rx * rx
            a2bx = a2b - lx * lx * rx

            ways = 0

            # Exactly one surrounding element equals x.
            # The other three values must be pairwise distinct.
            ways += lx * (A * DB - B * qx + ab2x)
            ways += rx * (B * DA - A * qx + a2bx)

            # Exactly two surrounding elements equal x.
            # The remaining two elements can have any values.
            ways += lx * rx * A * B
            ways += (lx * (lx - 1) // 2) * (B * (B - 1) // 2)
            ways += (rx * (rx - 1) // 2) * (A * (A - 1) // 2)

            # Exactly three surrounding elements equal x.
            ways += (lx * (lx - 1) // 2) * rx * B
            ways += lx * (rx * (rx - 1) // 2) * A

            # Exactly four surrounding elements equal x.
            ways += (lx * (lx - 1) // 2) * (rx * (rx - 1) // 2)

            answer = (answer + ways) % MOD

            # Move nums[j] to the left side for the next center.
            a = left.get(x, 0)
            b = right.get(x, 0)
            change(x, a + 1, b)
            left_size += 1

        return answer