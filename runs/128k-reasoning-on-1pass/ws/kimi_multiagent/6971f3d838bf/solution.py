from typing import List
from collections import defaultdict


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        NEG = -(1 << 60)  # "empty" sentinel: far below any reachable sum (|sum| <= 1e11)

        # ---------- iterative segment tree ----------
        # node = (total, best_prefix, best_suffix, best_subarray) over its range
        # identity (empty range) = (0, NEG, NEG, NEG)
        size = 1
        while size < n:
            size <<= 1

        T = [0] * (2 * size)
        P = [NEG] * (2 * size)
        S = [NEG] * (2 * size)
        B = [NEG] * (2 * size)

        for i in range(n):
            v = nums[i]
            j = size + i
            T[j] = v
            P[j] = v
            S[j] = v
            B[j] = v
        for i in range(size - 1, 0, -1):
            l = i << 1
            r = l | 1
            T[i] = T[l] + T[r]
            pl = P[l]; tp = T[l] + P[r]
            P[i] = pl if pl > tp else tp
            sr = S[r]; ts = T[r] + S[l]
            S[i] = sr if sr > ts else ts
            bb = B[l] if B[l] > B[r] else B[r]
            sp = S[l] + P[r]
            B[i] = bb if bb > sp else sp

        def query(l, r, base=size, T=T, P=P, S=S, B=B, NEG=NEG):
            """Aggregate of nums[l..r] inclusive -> (total, pref, suff, best)."""
            l += base
            r += base + 1
            # left / right accumulators, both start as the empty identity
            lat, lap, las, lab = 0, NEG, NEG, NEG
            rat, rap, ras, rab = 0, NEG, NEG, NEG
            while l < r:
                if l & 1:
                    # merge(left_acc, node l)
                    t = lat + T[l]
                    a = lap; b = lat + P[l]
                    p = a if a > b else b
                    a = S[l]; b = T[l] + las
                    s = a if a > b else b
                    a = lab if lab > B[l] else B[l]
                    b = las + P[l]
                    if b > a:
                        a = b
                    lat, lap, las, lab = t, p, s, a
                    l += 1
                if r & 1:
                    r -= 1
                    # merge(node r, right_acc)
                    t = T[r] + rat
                    a = P[r]; b = T[r] + rap
                    p = a if a > b else b
                    a = ras; b = rat + S[r]
                    s = a if a > b else b
                    a = B[r] if B[r] > rab else rab
                    b = S[r] + rap
                    if b > a:
                        a = b
                    rat, rap, ras, rab = t, p, s, a
                l >>= 1
                r >>= 1
            # merge(left_acc, right_acc)
            t = lat + rat
            a = lap; b = lat + rap
            p = a if a > b else b
            a = ras; b = rat + las
            s = a if a > b else b
            a = lab if lab > rab else rab
            b = las + rap
            if b > a:
                a = b
            return (t, p, s, a)

        def combine(A, Q):
            """merge(A, Q): aggregate of A's elements followed by Q's elements."""
            t = A[0] + Q[0]
            a = A[1]; b = A[0] + Q[1]
            p = a if a > b else b
            a = Q[2]; b = Q[0] + A[2]
            s = a if a > b else b
            a = A[3] if A[3] > Q[3] else Q[3]
            b = A[2] + Q[1]
            if b > a:
                a = b
            return (t, p, s, a)

        # ---------- prefix / suffix aggregates (O(1) endpoint gaps) ----------
        pre = [None] * n
        v = nums[0]
        pre[0] = (v, v, v, v)
        for i in range(1, n):
            v = nums[i]
            t, p, s, b = pre[i - 1]
            nt = t + v
            np_ = p if p > t + v else t + v
            ns = v if v > v + s else v + s
            nb = b if b > v else v
            c = s + v
            if c > nb:
                nb = c
            pre[i] = (nt, np_, ns, nb)

        suf = [None] * n
        v = nums[-1]
        suf[n - 1] = (v, v, v, v)
        for i in range(n - 2, -1, -1):
            v = nums[i]
            t, p, s, b = suf[i + 1]
            nt = v + t
            np_ = v if v > v + p else v + p
            ns = s if s > t + v else t + v
            nb = v if v > b else b
            c = v + p
            if c > nb:
                nb = c
            suf[i] = (nt, np_, ns, nb)

        # ---------- evaluate all possibilities ----------
        ans = pre[n - 1][3]  # no operation (also covers deleting a value not present)

        positions = defaultdict(list)
        for i, v in enumerate(nums):
            positions[v].append(i)

        ID = (0, NEG, NEG, NEG)
        for ps in positions.values():
            m = len(ps)
            if m == n:
                continue  # deletion would empty the array -> not allowed
            agg = ID
            if ps[0] > 0:                       # gap before first occurrence
                agg = pre[ps[0] - 1]
            for i in range(m - 1):              # gaps between consecutive occurrences
                a = ps[i] + 1
                b = ps[i + 1] - 1
                if a <= b:
                    agg = combine(agg, query(a, b))
            if ps[-1] < n - 1:                  # gap after last occurrence
                agg = combine(agg, suf[ps[-1] + 1])
            if agg[3] > ans:
                ans = agg[3]

        return ans