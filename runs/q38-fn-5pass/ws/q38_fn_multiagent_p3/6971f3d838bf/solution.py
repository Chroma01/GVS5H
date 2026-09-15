from typing import List

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        if not nums:
            return 0

        n = len(nums)
        NEG = -10**18

        positions = {}
        max_val = nums[0]

        for i, v in enumerate(nums):
            if v > max_val:
                max_val = v
            if v < 0:
                if v in positions:
                    positions[v].append(i)
                else:
                    positions[v] = [i]

        # Baseline: maximum subarray sum without any deletion.
        cur = NEG
        ans = NEG
        for v in nums:
            if cur == NEG:
                cur = v
            else:
                t = cur + v
                cur = v if v >= t else t
            if ans < cur:
                ans = cur

        # If all values are non-positive, deleting negatives cannot improve
        # the maximum element / zero baseline.
        if max_val <= 0:
            return ans

        single_neg = set()
        multi = []

        for v, lst in positions.items():
            l = len(lst)
            if l == 1:
                single_neg.add(v)
            elif l < n:
                multi.append(lst)

        # Fast exact handling for negative values that occur exactly once.
        if single_neg:
            end_at = [NEG] * n
            pref_best = [NEG] * n

            cur_end = NEG
            cur_best = NEG
            for i, v in enumerate(nums):
                pref_best[i] = cur_best

                if cur_end == NEG:
                    cur_end = v
                else:
                    t = cur_end + v
                    cur_end = v if v >= t else t

                end_at[i] = cur_end
                if cur_best < cur_end:
                    cur_best = cur_end

            start_at = [NEG] * n
            cur_start = NEG
            for i in range(n - 1, -1, -1):
                v = nums[i]
                if cur_start == NEG:
                    cur_start = v
                else:
                    t = v + cur_start
                    cur_start = v if v >= t else t
                start_at[i] = cur_start

            suf_best = NEG
            for i in range(n - 1, -1, -1):
                v = nums[i]

                if v < 0 and v in single_neg:
                    cand = pref_best[i]
                    if suf_best > cand:
                        cand = suf_best

                    if i > 0 and i + 1 < n:
                        cross = end_at[i - 1] + start_at[i + 1]
                        if cross > cand:
                            cand = cross

                    if cand > ans:
                        ans = cand

                if start_at[i] > suf_best:
                    suf_best = start_at[i]

        # Segment tree for negative values occurring multiple times.
        if multi:
            size = 1
            while size < n:
                size <<= 1

            total = size << 1
            sumv = [0] * total
            pref = [NEG] * total
            suff = [NEG] * total
            best = [NEG] * total

            for i, v in enumerate(nums):
                p = size + i
                sumv[p] = v
                pref[p] = v
                suff[p] = v
                best[p] = v

            for p in range(size - 1, 0, -1):
                l = p << 1
                r = l | 1

                sl = sumv[l]
                sr = sumv[r]
                sumv[p] = sl + sr

                pl = pref[l]
                pr = pref[r]
                t = sl + pr
                pref[p] = pl if pl >= t else t

                ss = suff[l]
                sr_s = suff[r]
                t = sr + ss
                suff[p] = sr_s if sr_s >= t else t

                bl = best[l]
                br = best[r]
                t = ss + pr
                if br > bl:
                    bl = br
                if t > bl:
                    bl = t
                best[p] = bl

            if best[1] > ans:
                ans = best[1]

            def update(
                i,
                active,
                sumv=sumv,
                pref=pref,
                suff=suff,
                best=best,
                nums=nums,
                size=size,
                NEG=NEG,
            ):
                p = size + i

                if active:
                    v = nums[i]
                    sumv[p] = v
                    pref[p] = v
                    suff[p] = v
                    best[p] = v
                else:
                    sumv[p] = 0
                    pref[p] = NEG
                    suff[p] = NEG
                    best[p] = NEG

                p >>= 1
                while p:
                    l = p << 1
                    r = l | 1

                    sl = sumv[l]
                    sr = sumv[r]
                    sumv[p] = sl + sr

                    pl = pref[l]
                    pr = pref[r]
                    t = sl + pr
                    pref[p] = pl if pl >= t else t

                    ss = suff[l]
                    sr_s = suff[r]
                    t = sr + ss
                    suff[p] = sr_s if sr_s >= t else t

                    bl = best[l]
                    br = best[r]
                    t = ss + pr
                    if br > bl:
                        bl = br
                    if t > bl:
                        bl = t
                    best[p] = bl

                    p >>= 1

            upd = update
            for indices in multi:
                for i in indices:
                    upd(i, False)

                if best[1] > ans:
                    ans = best[1]

                for i in indices:
                    upd(i, True)

        return ans