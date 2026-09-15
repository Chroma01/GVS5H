from typing import List
from collections import defaultdict

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)

        cntL = defaultdict(int)
        cntR = defaultdict(int)

        # totalC2L/R = sum over values v of C(count[v], 2)
        totalC2L = 0
        totalC2R = 0

        # For middle index k = 2, left side is indices 0, 1.
        for i in range(2):
            v = nums[i]
            c = cntL[v]
            totalC2L += c
            cntL[v] = c + 1

        # For middle index k = 2, right side is indices 3..n-1.
        for i in range(3, n):
            v = nums[i]
            c = cntR[v]
            totalC2R += c
            cntR[v] = c + 1

        ans = 0

        # Middle index k must have at least two elements before and after it.
        for k in range(2, n - 2):
            x = nums[k]

            left_size = k
            right_size = n - k - 1

            cntLx = cntL.get(x, 0)
            cntRx = cntR.get(x, 0)

            nonL = left_size - cntLx
            nonR = right_size - cntRx

            # Left pair categories: 2, 1, or 0 copies of x.
            L2 = cntLx * (cntLx - 1) // 2
            L1 = cntLx * nonL
            L0 = nonL * (nonL - 1) // 2

            # Right pair categories: 2, 1, or 0 copies of x.
            R2 = cntRx * (cntRx - 1) // 2
            R1 = cntRx * nonR
            R0 = nonR * (nonR - 1) // 2

            # Cases where x appears at least 3 times total: a + b >= 2.
            ans += L2 * (R0 + R1 + R2) + L1 * (R1 + R2) + L0 * R2

            # Case a + b = 1, left side contributes the single extra x.
            # Right side must contribute two distinct non-x values, neither equal
            # to the left side's non-x value y.
            if cntLx:
                # D_R = number of right-side pairs with zero x and two distinct values.
                D_R = (
                    nonR * (nonR - 1) // 2
                    - (totalC2R - cntRx * (cntRx - 1) // 2)
                )

                s = 0
                for y, cy in cntL.items():
                    if y == x or cy == 0:
                        continue

                    cyR = cntR.get(y, 0)

                    # Remove right-side distinct zero-x pairs that contain y.
                    valid_right_pairs = D_R - cyR * (nonR - cyR)
                    s += cy * valid_right_pairs

                ans += cntLx * s

            # Case a + b = 1, right side contributes the single extra x.
            # Left side must contribute two distinct non-x values, neither equal
            # to the right side's non-x value y.
            if cntRx:
                # D_L = number of left-side pairs with zero x and two distinct values.
                D_L = (
                    nonL * (nonL - 1) // 2
                    - (totalC2L - cntLx * (cntLx - 1) // 2)
                )

                s = 0
                for y, cy in cntR.items():
                    if y == x or cy == 0:
                        continue

                    cyL = cntL.get(y, 0)

                    # Remove left-side distinct zero-x pairs that contain y.
                    valid_left_pairs = D_L - cyL * (nonL - cyL)
                    s += cy * valid_left_pairs

                ans += cntRx * s

            ans %= MOD

            # No need to update after the last valid middle index.
            if k == n - 3:
                break

            # Move current middle index into the left side.
            v = nums[k]
            c = cntL[v]
            totalC2L += c
            cntL[v] = c + 1

            # Move next middle index out of the right side.
            v = nums[k + 1]
            c = cntR[v]
            totalC2R -= c - 1
            cntR[v] = c - 1
            if cntR[v] == 0:
                del cntR[v]

        return ans % MOD