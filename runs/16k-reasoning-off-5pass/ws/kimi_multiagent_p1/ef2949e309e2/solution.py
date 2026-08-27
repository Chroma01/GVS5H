from typing import List
from collections import defaultdict

MOD = 10**9 + 7

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        n = len(nums)

        def C2(k: int) -> int:
            return k * (k - 1) // 2 if k >= 2 else 0

        # Frequency maps: left of i and right of i (initially everything on right)
        Lc = defaultdict(int)
        Rc = defaultdict(int)
        for v in nums:
            Rc[v] += 1

        # Aggregate sums over ALL values v (we subtract x's contribution at query time)
        # P_L = sum_v C(Lc[v],2), P_R = sum_v C(Rc[v],2)
        # S1  = sum_v Lc[v]*Rc[v]
        # S2  = sum_v Lc[v]*Rc[v]^2
        # S3  = sum_v Lc[v]^2*Rc[v]
        P_L = 0
        P_R = 0
        S1 = 0
        S2 = 0
        S3 = 0
        for v, c in Rc.items():
            P_R += C2(c)

        ans = 0
        l = 0          # number of elements left of i
        r = n          # number of elements right of i (before removing nums[i])

        for i in range(n):
            x = nums[i]
            # Move x from right side to "current": it leaves Rc
            oldR = Rc[x]
            # Apply delta of Rc[x]: oldR -> oldR - 1 on aggregates
            cL = Lc[x]
            # P_R change: C(oldR,2) -> C(oldR-1,2): delta = -(oldR-1)
            P_R -= (oldR - 1)
            # S1: Lc*Rc term for x: cL*oldR -> cL*(oldR-1): delta = -cL
            S1 -= cL
            # S2: cL*oldR^2 -> cL*(oldR-1)^2: delta = cL*((oldR-1)^2 - oldR^2) = cL*(-2*oldR+1)
            S2 += cL * (-2 * oldR + 1)
            # S3: cL^2*oldR -> cL^2*(oldR-1): delta = -cL^2
            S3 -= cL * cL
            Rc[x] = oldR - 1
            r -= 1

            # Now query with middle index i, value x
            Lx = cL               # count of x strictly left of i
            Rx = Rc[x]            # count of x strictly right of i
            ln = l - Lx           # non-x count left
            rn = r - Rx           # non-x count right

            # Aggregates restricted to non-x values:
            # P_L' = P_L - C(Lx,2), P_R' = P_R - C(Rx,2)
            PLx = P_L - C2(Lx)
            PRx = P_R - C2(Rx)
            # S1' = S1 - Lx*Rx ; S2' = S2 - Lx*Rx^2 ; S3' = S3 - Lx^2*Rx
            S1x = S1 - Lx * Rx
            S2x = S2 - Lx * Rx * Rx
            S3x = S3 - Lx * Lx * Rx

            good = 0

            # ---- Cases a+b >= 2 (a from left, b from right are # of x's picked) ----
            # (a,b) in {(2,0),(0,2),(1,1),(2,1),(1,2),(2,2)}
            for a, b in ((2, 0), (0, 2), (1, 1), (2, 1), (1, 2), (2, 2)):
                ways = C2(Lx) if a == 2 else (Lx if a == 1 else 1)
                if a == 2:
                    ways = C2(Lx)
                elif a == 1:
                    ways = Lx
                else:
                    ways = 1
                wb = C2(Rx) if b == 2 else (Rx if b == 1 else 1)
                ways *= wb
                ways *= C2(ln) if (2 - a) == 2 else (ln if (2 - a) == 1 else 1)
                ways *= C2(rn) if (2 - b) == 2 else (rn if (2 - b) == 1 else 1)
                good += ways

            # ---- Case a=1, b=0: one x from left, one non-x from left, two non-x from right,
            #      the three non-x values pairwise distinct ----
            # = Lx * [ ln * D_R - (rn * S1' - S2') ]
            # where D_R = C(rn,2) - P_R'  (right 2-subsets with distinct non-x values)
            D_R = C2(rn) - PRx
            case10 = Lx * (ln * D_R - (rn * S1x - S2x))
            good += case10

            # ---- Case a=0, b=1: symmetric ----
            D_L = C2(ln) - PLx
            case01 = Rx * (rn * D_L - (ln * S1x - S3x))
            good += case01

            ans = (ans + good) % MOD

            # Move x into left map: Lc[x]: cL -> cL+1
            # P_L: delta = +cL  (C(cL+1,2)-C(cL,2) = cL)
            P_L += cL
            # S1: (cL+1)*Rx - cL*Rx = +Rx
            S1 += Rx
            # S2: ((cL+1)-cL)*Rx^2 = +Rx^2
            S2 += Rx * Rx
            # S3: ((cL+1)^2 - cL^2)*Rx = (2*cL+1)*Rx
            S3 += (2 * cL + 1) * Rx
            Lc[x] = cL + 1
            l += 1

        return ans % MOD