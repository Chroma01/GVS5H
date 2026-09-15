from typing import List
from collections import defaultdict


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)

        # prefix sums P[0..n]
        P = [0] * (n + 1)
        s = 0
        for i in range(n):
            s += nums[i]
            P[i + 1] = s

        # baseline: standard Kadane (no deletion)
        best = nums[0]
        cur = nums[0]
        for i in range(1, n):
            v = nums[i]
            cur = cur + v if cur > 0 else v
            if cur > best:
                best = cur
        ans = best

        # positions (1-indexed) grouped by value
        pos = defaultdict(list)
        for i in range(n):
            pos[nums[i]].append(i + 1)

        # removing the single distinct value would empty the array -> no-op only
        if len(pos) == 1:
            return ans

        # ---- sparse tables for range min / max over P ----
        m = n + 1                      # P has indices 0..n
        lg = [0] * (m + 1)
        for i in range(2, m + 1):
            lg[i] = lg[i >> 1] + 1

        stmin = [P]
        stmax = [P]
        level = 1
        while (1 << level) <= m:
            half = 1 << (level - 1)
            pm = stmin[-1]
            px = stmax[-1]
            stmin.append([a if a < b else b for a, b in zip(pm, pm[half:])])
            stmax.append([a if a > b else b for a, b in zip(px, px[half:])])
            level += 1

        # ---- for each value, evaluate only subarrays that span at least one occurrence ----
        for x, ps in pos.items():
            k = len(ps)
            if k == n:                 # deleting x empties the array
                continue

            # g = min over a in block 0 of Q_x(a) = P[a] - x*0
            l0, r0 = 0, ps[0] - 1
            L = lg[r0 - l0 + 1]
            a = stmin[L][l0]
            b = stmin[L][r0 - (1 << L) + 1]
            g = a if a < b else b

            for j in range(1, k + 1):
                start = ps[j - 1] + 1
                end = (ps[j] - 1) if j < k else n
                if start <= end:
                    L2 = lg[end - start + 1]
                    i2 = end - (1 << L2) + 1
                    # max P over non-x r in the block
                    a = stmax[L2][start]
                    b = stmax[L2][i2]
                    mx = a if a > b else b
                    cand = mx - x * j - g
                    if cand > ans:
                        ans = cand
                    # min P over the block (whole block needs P[p_j] too)
                    a = stmin[L2][start]
                    b = stmin[L2][i2]
                    mn = a if a < b else b
                    pv = P[ps[j - 1]]
                    if pv < mn:
                        mn = pv
                else:
                    mn = P[ps[j - 1]]
                val = mn - x * j
                if val < g:
                    g = val

        return ans