from typing import List
from collections import defaultdict


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)

        # ---------- Baseline: no operation (Kadane, non-empty subarray) ----------
        best_overall = nums[0]
        cur = nums[0]
        for v in nums[1:]:
            cur = v if cur + v < v else cur + v
            if cur > best_overall:
                best_overall = cur

        # ---------- Group indices by value ----------
        positions = defaultdict(list)
        for i, v in enumerate(nums):
            positions[v].append(i)

        # ---------- Iterative segment tree ----------
        # Node: (total, pref, suff, best) for the covered segment.
        # pref/suff/best refer to non-empty prefixes/suffixes/subarrays.
        size = 1
        while size < n:
            size <<= 1
        NEG = float('-inf')
        # identity element for combination (represents "empty segment")
        ID = (0, NEG, NEG, NEG)

        def combine(a, b):
            # a is left part, b is right part; b may be identity (empty)
            if b[3] == NEG and b[0] == 0:
                return a
            total = a[0] + b[0]
            pref = a[1] if a[1] >= a[0] + b[1] else a[0] + b[1]
            suff = b[2] if b[2] >= b[0] + a[2] else b[0] + a[2]
            cross = a[2] + b[1]
            best = a[3] if a[3] >= b[3] else b[3]
            if cross > best:
                best = cross
            return (total, pref, suff, best)

        tree = [ID] * (2 * size)
        for i in range(n):
            v = nums[i]
            tree[size + i] = (v, v, v, v)
        for i in range(size - 1, 0, -1):
            tree[i] = combine(tree[2 * i], tree[2 * i + 1])

        def query(l: int, r: int) -> int:
            # max subarray sum within nums[l..r] inclusive; requires l <= r
            l += size
            r += size
            left_res = ID
            right_res = ID
            while l <= r:
                if l & 1:
                    left_res = combine(left_res, tree[l])
                    l += 1
                if not (r & 1):
                    right_res = combine(tree[r], right_res)
                    r -= 1
                l >>= 1
                r >>= 1
            return combine(left_res, right_res)[3]

        # ---------- Try deleting each distinct negative value ----------
        for x, pos in positions.items():
            if x >= 0:
                continue  # deleting non-negatives can never help
            prev = -1
            for p in pos:
                if p - 1 >= prev + 1:
                    cand = query(prev + 1, p - 1)
                    if cand > best_overall:
                        best_overall = cand
                prev = p
            if n - 1 >= prev + 1:
                cand = query(prev + 1, n - 1)
                if cand > best_overall:
                    best_overall = cand

        return best_overall