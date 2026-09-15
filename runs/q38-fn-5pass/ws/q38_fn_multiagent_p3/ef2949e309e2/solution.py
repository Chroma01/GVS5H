from typing import List

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)

        # c2[i] = C(i, 2)
        c2 = [i * (i - 1) // 2 for i in range(n + 1)]

        left = {}
        right = {}
        for v in nums:
            right[v] = right.get(v, 0) + 1

        left_size = 0
        right_size = n

        # Number of index pairs with different values on each side.
        left_distinct = 0
        right_distinct = c2[n]
        for cnt in right.values():
            right_distinct -= c2[cnt]

        ans = 0

        for k, x in enumerate(nums):
            # Remove current element from the right side; it is the middle.
            cnt = right[x]
            right_distinct -= right_size - cnt
            if cnt == 1:
                del right[x]
            else:
                right[x] = cnt - 1
            right_size -= 1

            if left_size >= 2 and right_size >= 2:
                Lx = left.get(x, 0)
                Rx = right.get(x, 0)

                # If x does not appear on either side, it cannot be the mode.
                if Lx or Rx:
                    l = left_size
                    r = right_size
                    left_non_x = l - Lx
                    right_non_x = r - Rx

                    # Count choices where the side contains at least two x's.
                    # Start from all choices, subtract zero side-x and exactly one side-x.
                    valid = c2[l] * c2[r]
                    valid -= c2[left_non_x] * c2[right_non_x]
                    valid -= Lx * left_non_x * c2[right_non_x]
                    valid -= c2[left_non_x] * Rx * right_non_x

                    # Exactly one side-x on the left:
                    # left pair has one x and one non-x y; right pair has zero x,
                    # two distinct values, and neither equals y.
                    if Lx and left_non_x:
                        d_r_excl_x = right_distinct - Rx * right_non_x
                        bad_left = 0
                        rget = right.get
                        for y, ly in left.items():
                            if y == x:
                                continue
                            ry = rget(y, 0)
                            if ry:
                                bad_left += ly * ry * (right_non_x - ry)
                        valid += Lx * (d_r_excl_x * left_non_x - bad_left)

                    # Exactly one side-x on the right, symmetric.
                    if Rx and right_non_x:
                        d_l_excl_x = left_distinct - Lx * left_non_x
                        bad_right = 0
                        lget = left.get
                        for y, ry in right.items():
                            if y == x:
                                continue
                            ly = lget(y, 0)
                            if ly:
                                bad_right += ry * ly * (left_non_x - ly)
                        valid += Rx * (d_l_excl_x * right_non_x - bad_right)

                    ans = (ans + valid) % MOD

            # Move current element to the left side for future middle indices.
            cnt = left.get(x, 0)
            left_distinct += left_size - cnt
            left[x] = cnt + 1
            left_size += 1

        return ans