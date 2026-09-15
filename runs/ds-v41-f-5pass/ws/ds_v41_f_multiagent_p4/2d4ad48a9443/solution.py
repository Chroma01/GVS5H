import sys
from typing import List


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        sys.setrecursionlimit(1 << 20)
        n = len(nums)

        # global prefix sums of nums
        pref = [0] * (n + 1)
        s = 0
        for i in range(n):
            s += nums[i]
            pref[i + 1] = s

        TH = 20  # small segments handled by direct brute force

        def brute(lo, hi):
            cnt = 0
            nm = nums
            kk = k
            for L in range(lo, hi + 1):
                curmax = nm[L]
                cost = 0
                for R in range(L, hi + 1):
                    v = nm[R]
                    if v > curmax:
                        curmax = v
                    cost += curmax - v
                    if cost <= kk:
                        cnt += 1
                    else:
                        break  # cost is nondecreasing in R
            return cnt

        def solve(lo, hi):
            if hi - lo + 1 <= TH:
                return brute(lo, hi)

            mid = (lo + hi) >> 1
            # subarrays fully inside the two halves
            total = solve(lo, mid) + solve(mid + 1, hi)

            # right half: R[t] = max(nums[mid+1 .. mid+1+t]) is nondecreasing
            rlen = hi - mid
            R = [0] * rlen
            PM = [0] * (rlen + 1)            # PM[m] = sum R[0..m-1]
            cur = 0
            b = mid + 1
            for t in range(rlen):
                v = nums[b + t]
                if v > cur:
                    cur = v
                R[t] = cur
                PM[t + 1] = PM[t] + cur

            base = pref[mid + 1]             # sum nums[0..mid]
            rstar = hi                       # largest valid r for current l
            sv = []                          # block values, right->left (sv[0] = max)
            sc = []                          # block counts
            T = 0                            # sum of running maxima over [l..mid]
            ptr0 = 0                         # count of R[t] < H (monotone in l)
            cross = 0

            for l in range(mid, lo - 1, -1):
                v = nums[l]
                absorbed = 1
                while sv and sv[-1] < v:
                    tv = sv.pop()
                    tc = sc.pop()
                    T -= tv * tc
                    absorbed += tc
                sv.append(v)
                sc.append(absorbed)
                T += v * absorbed

                H = sv[0]                     # max(nums[l..mid])
                A_l = T - (base - pref[l])    # cost of the left part alone

                while ptr0 < rlen and R[ptr0] < H:
                    ptr0 += 1
                t0 = ptr0

                while rstar > mid:
                    c = rstar - mid           # number of right elements
                    if t0 < c:
                        sumMax = H * t0 + (PM[c] - PM[t0])
                    else:
                        sumMax = H * c
                    if A_l + sumMax - (pref[rstar + 1] - base) <= k:
                        break
                    rstar -= 1

                if rstar > mid:
                    cross += rstar - mid
                else:
                    break  # larger l-costs for smaller l -> none feasible

            return total + cross

        return solve(0, n - 1)