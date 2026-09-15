from typing import List


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)

        # If every element is negative, no operation (or any operation) can beat
        # the largest single element, so return it.
        mx = max(nums)
        if mx < 0:
            return mx

        # Prefix sums P[0..n].
        P = [0] * (n + 1)
        s = 0
        for i in range(n):
            s += nums[i]
            P[i + 1] = s

        # Candidate: perform no operation.  Kadane allowing the empty subarray;
        # since mx >= 0 this equals the true (non-empty) maximum subarray.
        ans = 0
        cur = 0
        for v in nums:
            cur += v
            if cur < 0:
                cur = 0
            if cur > ans:
                ans = cur

        # Indices grouped by value.
        pos = {}
        for i in range(n):
            v = nums[i]
            if v in pos:
                pos[v].append(i)
            else:
                pos[v] = [i]

        # Sparse tables for range maximum / minimum over P (idempotent ops).
        m = n + 1
        stmax = [P]
        stmin = [P]
        k = 1
        while (1 << k) <= m:
            half = 1 << (k - 1)
            size = m - (1 << k) + 1
            pm = stmax[k - 1]
            pn = stmin[k - 1]
            lm = [0] * size
            ln = [0] * size
            for i in range(size):
                a = pm[i]
                b = pm[i + half]
                lm[i] = a if a > b else b
                a = pn[i]
                b = pn[i + half]
                ln[i] = a if a < b else b
            stmax.append(lm)
            stmin.append(ln)
            k += 1

        for v, idxs in pos.items():
            if len(idxs) == n:
                # Removing this value empties the array: not allowed.
                continue

            # Ordered gaps between occurrences of v (including the two ends).
            suf = 0       # best suffix sum of the concatenation processed so far
            bestx = 0     # best spanning subarray sum for this value
            prev = 0
            for idx in idxs + [n]:
                l = prev
                r = idx - 1
                if l <= r:
                    length = r - l + 1
                    kk = length.bit_length() - 1
                    shift = 1 << kk

                    # total of the gap
                    t = P[r + 1] - P[l]

                    # best prefix of the gap: max P over [l+1, r+1], minus P[l]
                    row = stmax[kk]
                    a = row[l + 1]
                    b = row[r + 2 - shift]
                    pmax = a if a > b else b
                    p = pmax - P[l]
                    if p < 0:
                        p = 0

                    # best suffix of the gap: P[r+1] minus min P over [l, r]
                    row = stmin[kk]
                    a = row[l]
                    b = row[r - shift + 1]
                    pmin = a if a < b else b
                    ss = P[r + 1] - pmin
                    if ss < 0:
                        ss = 0

                    cand = suf + p
                    if cand > bestx:
                        bestx = cand
                    tmp = suf + t
                    if ss > tmp:
                        tmp = ss
                    suf = tmp

                prev = idx + 1

            if bestx > ans:
                ans = bestx

        return ans