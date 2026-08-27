from typing import List

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)

        # Baseline: best non-empty subarray sum in the original array.
        best = nums[0]
        cur = nums[0]
        for v in nums[1:]:
            if cur < 0:
                cur = v
            else:
                cur += v
            if cur > best:
                best = cur

        # If there is no positive subarray, deleting a negative value cannot create one.
        if best <= 0:
            return best

        # Prefix sums and positions of negative values.
        pref = [0] * (n + 1)
        pos = {}
        s = 0
        for i, v in enumerate(nums):
            s += v
            pref[i + 1] = s
            if v < 0:
                pos.setdefault(v, []).append(i)

        if not pos:
            return best

        # Prefix minima and suffix maxima of original prefix sums.
        pref_min = [0] * (n + 1)
        mn = pref[0]
        for i in range(n + 1):
            if pref[i] < mn:
                mn = pref[i]
            pref_min[i] = mn

        suff_max = [0] * (n + 1)
        mx = pref[n]
        for i in range(n, -1, -1):
            if pref[i] > mx:
                mx = pref[i]
            suff_max[i] = mx

        INF = 10 ** 30

        # Segment tree for range min/max of pref, needed only for middle gaps.
        if any(len(lst) >= 2 for lst in pos.values()):
            size = 1
            while size < n + 1:
                size <<= 1

            minv = [INF] * (2 * size)
            maxv = [-INF] * (2 * size)

            for i, val in enumerate(pref):
                minv[size + i] = val
                maxv[size + i] = val

            for i in range(size - 1, 0, -1):
                left = i << 1
                right = left | 1
                minv[i] = minv[left] if minv[left] < minv[right] else minv[right]
                maxv[i] = maxv[left] if maxv[left] > maxv[right] else maxv[right]

            def range_min_max(l: int, r: int):
                if l == r:
                    return pref[l], pref[l]

                l += size
                r += size
                mn = INF
                mx = -INF

                while l <= r:
                    if l & 1:
                        if minv[l] < mn:
                            mn = minv[l]
                        if maxv[l] > mx:
                            mx = maxv[l]
                        l += 1

                    if not (r & 1):
                        if minv[r] < mn:
                            mn = minv[r]
                        if maxv[r] > mx:
                            mx = maxv[r]
                        r -= 1

                    l >>= 1
                    r >>= 1

                return mn, mx
        else:
            def range_min_max(l: int, r: int):
                return pref[l], pref[l]

        ans = best

        for x, p in pos.items():
            y = -x
            m = len(p)

            # First gap: prefix indices [0, p[0]], offset 0.
            min_seen = pref_min[p[0]]
            offset = y

            # Middle gaps: [p[k-1] + 1, p[k]], offset y * k.
            for k in range(1, m):
                l = p[k - 1] + 1
                r = p[k]
                minP, maxP = range_min_max(l, r)

                cand = maxP + offset - min_seen
                if cand > ans:
                    ans = cand

                minA = minP + offset
                if minA < min_seen:
                    min_seen = minA

                offset += y

            # Last gap: [p[-1] + 1, n], offset y * m.
            cand = suff_max[p[-1] + 1] + offset - min_seen
            if cand > ans:
                ans = cand

        return ans