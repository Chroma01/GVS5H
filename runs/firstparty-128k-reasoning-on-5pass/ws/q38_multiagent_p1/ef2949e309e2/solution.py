from typing import List
from collections import Counter

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        if n < 5:
            return 0

        def c2(t: int) -> int:
            return t * (t - 1) // 2

        ans = 0

        for m in range(2, n - 2):
            x = nums[m]

            lc = Counter(nums[:m])
            rc = Counter(nums[m + 1:])

            lx = lc.pop(x, 0)
            rx = rc.pop(x, 0)

            ln = 0
            sum_sq_l = 0
            for v in lc.values():
                ln += v
                sum_sq_l += v * v

            rn = 0
            sum_sq_r = 0
            for v in rc.values():
                rn += v
                sum_sq_r += v * v

            L0 = c2(ln)
            L1 = lx * ln
            L2 = c2(lx)

            R0 = c2(rn)
            R1 = rx * rn
            R2 = c2(rx)

            case_a = (
                L0 * R2
                + L1 * R1
                + L1 * R2
                + L2 * R0
                + L2 * R1
                + L2 * R2
            )

            d_left = (ln * ln - sum_sq_l) // 2
            d_right = (rn * rn - sum_sq_r) // 2

            case_b = 0

            if lx:
                s = 0
                for y, cy in lc.items():
                    rcy = rc.get(y, 0)
                    s += cy * (d_right - rcy * (rn - rcy))
                case_b += lx * s

            if rx:
                s = 0
                for y, cy in rc.items():
                    lcy = lc.get(y, 0)
                    s += cy * (d_left - lcy * (ln - lcy))
                case_b += rx * s

            ans = (ans + case_a + case_b) % MOD

        return ans