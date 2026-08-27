from typing import List
from collections import Counter


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 1_000_000_007
        n = len(nums)

        right = Counter(nums)
        R = n
        D_right = R * (R - 1) // 2 - sum(c * (c - 1) // 2 for c in right.values())

        left = {}
        L = 0
        D_left = 0
        ans = 0

        def c2(x: int) -> int:
            return x * (x - 1) // 2

        for v in nums:
            # Remove nums[k] from the right side so right contains indices > k.
            c = right[v]
            D_right -= R - c
            if c == 1:
                del right[v]
            else:
                right[v] = c - 1
            R -= 1

            if L >= 2 and R >= 2:
                lv = left.get(v, 0)
                rv = right.get(v, 0)
                ln = L - lv
                rn = R - rv

                # Cases where total count of v is 3, 4, or 5.
                term = (
                    c2(lv) * c2(rv)          # left 2 v, right 2 v
                    + c2(lv) * rv * rn       # left 2 v, right 1 v + 1 non-v
                    + lv * ln * c2(rv)       # left 1 v + 1 non-v, right 2 v
                    + c2(lv) * c2(rn)        # left 2 v, right 2 non-v
                    + lv * ln * rv * rn      # left 1 v + 1 non-v, right 1 v + 1 non-v
                    + c2(ln) * c2(rv)        # left 2 non-v, right 2 v
                )

                # Case: total count of v is 2, extra v on the left.
                # The three non-v values must be pairwise distinct.
                if lv:
                    Drn = D_right - rv * rn
                    s = 0
                    for x, lx in left.items():
                        if x == v:
                            continue
                        rx = right.get(x, 0)
                        s += lx * (Drn - rx * (rn - rx))
                    term += lv * s

                # Case: total count of v is 2, extra v on the right.
                # The three non-v values must be pairwise distinct.
                if rv:
                    Dln = D_left - lv * ln
                    s = 0
                    for y, ry in right.items():
                        if y == v:
                            continue
                        ly = left.get(y, 0)
                        s += ry * (Dln - ly * (ln - ly))
                    term += rv * s

                ans = (ans + term) % MOD

            # Add nums[k] to the left side for future middle positions.
            c = left.get(v, 0)
            D_left += L - c
            left[v] = c + 1
            L += 1

        return ans