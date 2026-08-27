from typing import List
from collections import Counter

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 1_000_000_007
        n = len(nums)
        ans = 0

        def c2(k: int) -> int:
            return k * (k - 1) // 2

        for i in range(2, n - 2):
            x = nums[i]
            left = Counter(nums[:i])
            right = Counter(nums[i + 1:])

            Lx = left.get(x, 0)
            Rx = right.get(x, 0)
            nonL = i - Lx
            nonR = n - i - 1 - Rx

            L0 = c2(nonL)
            L1 = Lx * nonL
            L2 = c2(Lx)
            R0 = c2(nonR)
            R1 = Rx * nonR
            R2 = c2(Rx)

            ans += (L2 * R0 + L2 * R1 + L2 * R2 +
                    L1 * R1 + L1 * R2 + L0 * R2)

            D_L = L0
            for v, c in left.items():
                if v != x:
                    D_L -= c2(c)

            D_R = R0
            for v, c in right.items():
                if v != x:
                    D_R -= c2(c)

            if Lx:
                s = 0
                for y, ly in left.items():
                    if y != x:
                        ry = right.get(y, 0)
                        s += ly * (D_R - ry * (nonR - ry))
                ans += Lx * s

            if Rx:
                s = 0
                for z, rz in right.items():
                    if z != x:
                        lz = left.get(z, 0)
                        s += rz * (D_L - lz * (nonL - lz))
                ans += Rx * s

            ans %= MOD

        return ans % MOD