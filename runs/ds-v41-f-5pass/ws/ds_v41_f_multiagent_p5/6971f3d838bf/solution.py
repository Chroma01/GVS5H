from typing import List

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        NEG = -10**15
        size = 1
        while size < n:
            size <<= 1
        total = 2 * size
        sum_arr = [0] * total
        pref = [NEG] * total
        suff = [NEG] * total
        best = [NEG] * total

        for i in range(n):
            v = nums[i]
            idx = size + i
            sum_arr[idx] = v
            pref[idx] = v
            suff[idx] = v
            best[idx] = v

        for i in range(size - 1, 0, -1):
            l = i << 1
            r = l | 1
            sl = sum_arr[l]
            sr = sum_arr[r]
            sum_arr[i] = sl + sr
            p = pref[l]
            alt = sl + pref[r]
            pref[i] = p if p >= alt else alt
            s = suff[r]
            alt2 = sr + suff[l]
            suff[i] = s if s >= alt2 else alt2
            b = best[l]
            br = best[r]
            if br > b:
                b = br
            cross = suff[l] + pref[r]
            if cross > b:
                b = cross
            best[i] = b

        ans = best[1]

        pos = {}
        for i, v in enumerate(nums):
            if v < 0:
                if v in pos:
                    pos[v].append(i)
                else:
                    pos[v] = [i]

        max1 = max(nums)
        max2 = -10**18
        for v in nums:
            if v != max1 and v > max2:
                max2 = v

        for v, indices in pos.items():
            if len(indices) == n:
                continue
            # deactivate
            for i in indices:
                idx = size + i
                sum_arr[idx] = 0
                pref[idx] = 0
                suff[idx] = 0
                best[idx] = 0
                j = idx >> 1
                while j:
                    l = j << 1
                    r = l | 1
                    sl = sum_arr[l]
                    sr = sum_arr[r]
                    sum_arr[j] = sl + sr
                    p = pref[l]
                    alt = sl + pref[r]
                    pref[j] = p if p >= alt else alt
                    s = suff[r]
                    alt2 = sr + suff[l]
                    suff[j] = s if s >= alt2 else alt2
                    b = best[l]
                    br = best[r]
                    if br > b:
                        b = br
                    cross = suff[l] + pref[r]
                    if cross > b:
                        b = cross
                    best[j] = b
                    j >>= 1
            M = best[1]
            max_nonx = max1 if max1 != v else max2
            candidate = M if M > 0 else max_nonx
            if candidate > ans:
                ans = candidate
            # restore
            for i in indices:
                idx = size + i
                val = v
                sum_arr[idx] = val
                pref[idx] = val
                suff[idx] = val
                best[idx] = val
                j = idx >> 1
                while j:
                    l = j << 1
                    r = l | 1
                    sl = sum_arr[l]
                    sr = sum_arr[r]
                    sum_arr[j] = sl + sr
                    p = pref[l]
                    alt = sl + pref[r]
                    pref[j] = p if p >= alt else alt
                    s = suff[r]
                    alt2 = sr + suff[l]
                    suff[j] = s if s >= alt2 else alt2
                    b = best[l]
                    br = best[r]
                    if br > b:
                        b = br
                    cross = suff[l] + pref[r]
                    if cross > b:
                        b = cross
                    best[j] = b
                    j >>= 1

        return ans