from typing import List
from collections import defaultdict

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        max_elem = max(nums)

        # If there is no positive element, deleting negatives cannot create
        # a better positive sum; the best subarray is just the maximum element.
        if max_elem <= 0:
            return max_elem

        # Group negative values and compute the original Kadane answer.
        pos = defaultdict(list)
        positive_sum = 0
        cur = 0
        ans = -10**30

        for i, v in enumerate(nums):
            if v > 0:
                positive_sum += v
            elif v < 0:
                pos[v].append(i)

            if cur > 0:
                cur += v
            else:
                cur = v
            if cur > ans:
                ans = cur

        # No negative deletion candidate, or already at the absolute upper bound.
        if not pos or ans == positive_sum:
            return ans

        base_ans = ans

        # Safe pruning: for value x, any interval can gain at most
        # count_x * |x| over its original sum, and original sum <= base_ans.
        candidates = []
        for x, occ in pos.items():
            if base_ans + len(occ) * (-x) > ans:
                candidates.append((x, occ))

        if not candidates:
            return ans

        # Iterative segment tree with four arrays:
        # sum, best non-empty prefix, best non-empty suffix, best non-empty subarray.
        size = 1
        while size < n:
            size <<= 1

        NEG_INF = -10**30
        total = size << 1

        sum_tree = [0] * total
        pref_tree = [NEG_INF] * total
        suff_tree = [NEG_INF] * total
        best_tree = [NEG_INF] * total

        base = size
        for i, v in enumerate(nums):
            idx = base + i
            sum_tree[idx] = v
            pref_tree[idx] = v
            suff_tree[idx] = v
            best_tree[idx] = v

        for idx in range(base - 1, 0, -1):
            left = idx << 1
            right = left | 1

            s1 = sum_tree[left]
            pre1 = pref_tree[left]
            suf1 = suff_tree[left]
            best1 = best_tree[left]

            s2 = sum_tree[right]
            pre2 = pref_tree[right]
            suf2 = suff_tree[right]
            best2 = best_tree[right]

            s = s1 + s2

            t = s1 + pre2
            pre = pre1 if pre1 >= t else t

            t = s2 + suf1
            suf = suf2 if suf2 >= t else t

            best = best1 if best1 >= best2 else best2
            t = suf1 + pre2
            if t > best:
                best = t

            sum_tree[idx] = s
            pref_tree[idx] = pre
            suff_tree[idx] = suf
            best_tree[idx] = best

        st = sum_tree
        pt = pref_tree
        sut = suff_tree
        bt = best_tree
        arr = nums
        sz = size

        for x, occ in candidates:
            # Re-check pruning because ans may have improved.
            if base_ans + len(occ) * (-x) <= ans:
                continue

            # Temporarily replace all occurrences of x by zero.
            for pos_idx in occ:
                idx = sz + pos_idx
                st[idx] = 0
                pt[idx] = 0
                sut[idx] = 0
                bt[idx] = 0

                idx >>= 1
                while idx:
                    left = idx << 1
                    right = left | 1

                    s1 = st[left]
                    pre1 = pt[left]
                    suf1 = sut[left]
                    best1 = bt[left]

                    s2 = st[right]
                    pre2 = pt[right]
                    suf2 = sut[right]
                    best2 = bt[right]

                    s = s1 + s2

                    t = s1 + pre2
                    pre = pre1 if pre1 >= t else t

                    t = s2 + suf1
                    suf = suf2 if suf2 >= t else t

                    best = best1 if best1 >= best2 else best2
                    t = suf1 + pre2
                    if t > best:
                        best = t

                    st[idx] = s
                    pt[idx] = pre
                    sut[idx] = suf
                    bt[idx] = best

                    idx >>= 1

            val = bt[1]
            if val > ans:
                ans = val
                if ans == positive_sum:
                    return ans

            # Restore original values.
            for pos_idx in occ:
                v = arr[pos_idx]
                idx = sz + pos_idx
                st[idx] = v
                pt[idx] = v
                sut[idx] = v
                bt[idx] = v

                idx >>= 1
                while idx:
                    left = idx << 1
                    right = left | 1

                    s1 = st[left]
                    pre1 = pt[left]
                    suf1 = sut[left]
                    best1 = bt[left]

                    s2 = st[right]
                    pre2 = pt[right]
                    suf2 = sut[right]
                    best2 = bt[right]

                    s = s1 + s2

                    t = s1 + pre2
                    pre = pre1 if pre1 >= t else t

                    t = s2 + suf1
                    suf = suf2 if suf2 >= t else t

                    best = best1 if best1 >= best2 else best2
                    t = suf1 + pre2
                    if t > best:
                        best = t

                    st[idx] = s
                    pt[idx] = pre
                    sut[idx] = suf
                    bt[idx] = best

                    idx >>= 1

        return ans