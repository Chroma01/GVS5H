from typing import List
from collections import defaultdict

MOD = 10**9 + 7

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        n = len(nums)
        if n < 5:
            return 0

        def C2(x: int) -> int:
            return x * (x - 1) // 2

        # Frequency maps
        cntL = defaultdict(int)
        cntR = defaultdict(int)
        for x in nums:
            cntR[x] += 1

        # Aggregates:
        # SumC2L = sum over values of C(cntL,2), similarly SumC2R
        # T1 = sum cntL[a]*cntR[a]
        # T2 = sum cntL[a]*cntR[a]^2
        SumC2L = 0
        SumC2R = sum(C2(c) for c in cntR.values())
        T1 = 0  # cntL all zero initially
        T2 = 0

        ans = 0

        for i in range(n):
            v = nums[i]
            # Move v from right to "current" (remove from right side)
            oldR = cntR[v]
            SumC2R -= C2(oldR)
            # T1, T2 lose cntL[v]*oldR terms (cntL[v] currently is count before adding v)
            lv = cntL[v]
            T1 -= lv * oldR
            T2 -= lv * oldR * oldR
            cntR[v] = oldR - 1
            SumC2R += C2(oldR - 1)
            # after decrement, cntR[v] = oldR-1; T1/T2 currently exclude v entirely (we removed its contribution)

            L = i              # number of elements on left (not including i)
            R = n - 1 - i      # number of elements on right

            if L >= 2 and R >= 2:
                l = cntL[v]        # copies of v on left
                r = cntR[v]        # copies of v on right (after removal)
                Lp = L - l         # left elements != v
                Rp = R - r         # right elements != v

                # T1', T2' excluding value v (currently T1,T2 have v's contribution removed)
                T1p = T1
                T2p = T2

                # P_right: unordered pairs from right, both != v, distinct values
                P_right = C2(Rp) - (SumC2R - C2(r))
                # P_left: unordered pairs from left, both != v, distinct values
                P_left = C2(Lp) - (SumC2L - C2(l))

                # k=4: both left picks = v, both right picks = v
                ans += C2(l) * C2(r)

                # k=3: exactly 3 copies of v among 4 picks
                # two v's from left, one v from right, one non-v from right
                ans += C2(l) * r * Rp
                # two v's from right, one v from left, one non-v from left
                ans += C2(r) * l * Lp

                # k=2: exactly 2 copies of v among 4 picks (always valid)
                # both v's on left, two non-v on right
                ans += C2(l) * C2(Rp)
                # both v's on right, two non-v on left
                ans += C2(r) * C2(Lp)
                # one v each side, one non-v each side
                ans += l * r * Lp * Rp

                # k=1: exactly one copy of v among picks; other 3 picks pairwise distinct, != v
                # v-copy on left: choose which left position is v: l ways;
                #   1 non-v from left (a), 2 non-v from right distinct and != a
                #   sum over left elements a != v of [P_right - cntR[a]*(Rp - cntR[a])]
                #   = Lp*P_right - (Rp*T1' - T2')
                trip_1L2R = Lp * P_right - (Rp * T1p - T2p)
                ans += l * trip_1L2R

                # v-copy on right: r ways; 2 distinct non-v from left, 1 non-v from right != them
                trip_2L1R = Rp * P_left - (Lp * T1p - T2p)
                ans += r * trip_2L1R

                ans %= MOD

            # Now move v into left map (restore T1,T2 contributions with new cntL)
            newL = cntL[v] + 1
            rv = cntR[v]
            SumC2L -= C2(cntL[v])
            cntL[v] = newL
            SumC2L += C2(newL)
            T1 += newL * rv
            T2 += newL * rv * rv

        return ans % MOD