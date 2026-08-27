from typing import List


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)

        # Prefix sums PS[t] = sum(nums[0..t-1]), t = 0..n
        PS = [0] * (n + 1)
        s = 0
        for i, v in enumerate(nums):
            s += v
            PS[i + 1] = s

        # Kadane: max subarray sum of the original array (no deletion)
        best = nums[0]
        cur = nums[0]
        for i in range(1, n):
            v = nums[i]
            cur = v if v > cur + v else cur + v
            if cur > best:
                best = cur
        ans = best

        # Group positions of negative values (only deleting negatives can help)
        positions = {}
        for i, v in enumerate(nums):
            if v < 0:
                if v in positions:
                    positions[v].append(i)
                else:
                    positions[v] = [i]

        if not positions:
            return ans

        # Segment trees for range-min and range-max over PS (length m = n+1)
        m = n + 1
        size = 1
        while size < m:
            size <<= 1
        INF = 10 ** 30
        tmin = [INF] * (2 * size)
        tmax = [-INF] * (2 * size)
        tmin[size:size + m] = PS
        tmax[size:size + m] = PS
        for i in range(size - 1, 0, -1):
            a = tmin[i << 1]
            b = tmin[(i << 1) | 1]
            tmin[i] = a if a < b else b
            a = tmax[i << 1]
            b = tmax[(i << 1) | 1]
            tmax[i] = a if a > b else b

        tmin_l = tmin
        tmax_l = tmax
        sz = size
        INFV = INF

        def rmin(l, r):
            # inclusive [l, r]
            res = INFV
            l += sz
            r += sz + 1
            while l < r:
                if l & 1:
                    v = tmin_l[l]
                    if v < res:
                        res = v
                    l += 1
                if r & 1:
                    r -= 1
                    v = tmin_l[r]
                    if v < res:
                        res = v
                l >>= 1
                r >>= 1
            return res

        def rmax(l, r):
            # inclusive [l, r]
            res = -INFV
            l += sz
            r += sz + 1
            while l < r:
                if l & 1:
                    v = tmax_l[l]
                    if v > res:
                        res = v
                    l += 1
                if r & 1:
                    r -= 1
                    v = tmax_l[r]
                    if v > res:
                        res = v
                l >>= 1
                r >>= 1
            return res

        # For each distinct negative value x:
        # Filtered subarray sums = (PS[j] - PS[i]) - x*(cntX[j] - cntX[i])
        # = A[j] - A[i], with A[t] = PS[t] - x*cntX[t].
        # Blocks of t with constant cntX are the gaps between occurrences of x.
        # Cross-block pairs (i in earlier block, j in later block) are the only
        # ones that can beat the no-delete answer; sweep blocks maintaining the
        # minimum A[i] seen so far.
        for x, pos in positions.items():
            k = len(pos)
            if k == n:
                continue  # deleting x would empty the array (not allowed)
            minA = INFV
            bestx = -INFV
            prev = -1
            for mi in range(k + 1):
                a = prev + 1
                b = pos[mi] if mi < k else n
                # block t in [a..b], cntX = mi
                if mi >= 1:
                    jv = a + 1  # t = a corresponds to nums[a-1] == x, invalid as j
                    if jv <= b:
                        qmax = rmax(jv, b)
                        cand = qmax - x * mi - minA
                        if cand > bestx:
                            bestx = cand
                qmin = rmin(a, b)
                val = qmin - x * mi
                if val < minA:
                    minA = val
                if mi < k:
                    prev = pos[mi]
            if bestx > ans:
                ans = bestx

        return ans