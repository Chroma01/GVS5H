from typing import List


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]

        # ---------- baseline: plain non-empty Kadane on the original array ----------
        best = cur = nums[0]
        for i in range(1, n):
            v = nums[i]
            cur = v if cur < 0 else cur + v
            if cur > best:
                best = cur
        ans = best

        # ---------- only removing a NEGATIVE value can ever help ----------
        pos = {}
        for i in range(n):
            v = nums[i]
            if v < 0:
                lst = pos.get(v)
                if lst is None:
                    pos[v] = [i]
                else:
                    lst.append(i)
        if not pos:
            return ans

        # ---------- prefix sums ----------
        S = [0] * (n + 1)
        t = 0
        for i in range(n):
            t += nums[i]
            S[i + 1] = t

        # ---------- sparse tables (range max / range min over S) ----------
        m = n + 1
        mxs = [S]
        mns = [S]
        step = 1
        while step * 2 <= m:
            pmx = mxs[-1]
            pmn = mns[-1]
            mxs.append(list(map(max, pmx, pmx[step:])))
            mns.append(list(map(min, pmn, pmn[step:])))
            step <<= 1

        nm1 = n - 1
        for ps in pos.values():
            k = len(ps)
            A = None  # best residual-subarray sum ending exactly at the end of the last processed gap
            for j in range(k + 1):
                l = ps[j - 1] + 1 if j else 0
                r = ps[j] - 1 if j < k else nm1
                if l > r:
                    continue  # empty gap (consecutive / boundary occurrences)
                Sl = S[l]
                Sr1 = S[r + 1]
                kk = (r - l + 1).bit_length() - 1
                off = 1 << kk

                # best prefix of the gap = max_{i in [l,r]} (S[i+1]-S[l])
                a = mxs[kk]
                u = a[l + 1]
                w = a[r + 2 - off]
                bp = (u if u > w else w) - Sl

                if A is not None:
                    c = A + bp  # subarray crossing at least one removal boundary
                    if c > ans:
                        ans = c

                # best suffix of the gap = S[r+1] - min_{i in [l,r]} S[i]
                b = mns[kk]
                u = b[l]
                w = b[r + 1 - off]
                bs = Sr1 - (u if u < w else w)

                if A is None:
                    A = bs
                else:
                    nA = A + (Sr1 - Sl)
                    A = bs if bs > nA else nA

        return ans