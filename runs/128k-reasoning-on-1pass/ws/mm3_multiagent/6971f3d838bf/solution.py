import sys
from typing import List
from collections import defaultdict

class SegTree:
    def __init__(self, arr: List[int]):
        self.n = len(arr)
        size = 1
        while size < self.n:
            size <<= 1
        self.size = size
        self.sum = [0] * (2 * size)
        self.pref = [0] * (2 * size)
        self.suff = [0] * (2 * size)
        self.best = [0] * (2 * size)

        for i, v in enumerate(arr):
            p = size + i
            self.sum[p] = self.pref[p] = self.suff[p] = self.best[p] = v

        for p in range(size - 1, 0, -1):
            self._pull(p)

    def _pull(self, p: int):
        l = p << 1
        r = l | 1
        self.sum[p] = self.sum[l] + self.sum[r]
        self.pref[p] = max(self.pref[l], self.sum[l] + self.pref[r])
        self.suff[p] = max(self.suff[r], self.sum[r] + self.suff[l])
        self.best[p] = max(self.best[l], self.best[r],
                           self.suff[l] + self.pref[r])

    def query(self, l: int, r: int):
        l += self.size
        r += self.size
        left_res = None
        right_res = None
        while l <= r:
            if l & 1:
                node = (self.sum[l], self.pref[l],
                        self.suff[l], self.best[l])
                left_res = node if left_res is None else self._combine(left_res, node)
                l += 1
            if not (r & 1):
                node = (self.sum[r], self.pref[r],
                        self.suff[r], self.best[r])
                right_res = node if right_res is None else self._combine(node, right_res)
                r -= 1
            l //= 2
            r //= 2
        if left_res is None:
            return right_res
        if right_res is None:
            return left_res
        return self._combine(left_res, right_res)

    @staticmethod
    def _combine(a, b):
        s = a[0] + b[0]
        pref = max(a[1], a[0] + b[1])
        suff = max(b[2], b[0] + a[2])
        best = max(a[3], b[3], a[2] + b[1])
        return (s, pref, suff, best)


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        seg = SegTree(nums)

        # original answer (no operation)
        ans = seg.query(0, n - 1)[3]

        # collect positions of each distinct value
        pos = defaultdict(list)
        for i, v in enumerate(nums):
            pos[v].append(i)

        NEG_INF = -10**30

        for x, positions in pos.items():
            blocks = []
            prev = 0
            for p in positions:
                if p > prev:
                    node = seg.query(prev, p - 1)
                    blocks.append(node)
                prev = p + 1
            if prev < n:
                node = seg.query(prev, n - 1)
                blocks.append(node)

            # if deleting x would empty the array, skip
            if not blocks:
                continue

            m = len(blocks)
            total = [b[0] for b in blocks]
            pref  = [b[1] for b in blocks]
            suff  = [b[2] for b in blocks]
            best  = [b[3] for b in blocks]

            # best subarray completely inside one block
            best_overall = max(best)

            # prefix sums of block totals
            pref_sum = [0] * (m + 1)
            for i in range(m):
                pref_sum[i + 1] = pref_sum[i] + total[i]

            # linear scan for subarrays spanning multiple blocks
            best_A = NEG_INF
            for j in range(m):
                if j > 0:
                    cand = best_A + pref_sum[j] + pref[j]
                    if cand > best_overall:
                        best_overall = cand
                val = suff[j] - pref_sum[j + 1]
                if val > best_A:
                    best_A = val

            if best_overall > ans:
                ans = best_overall

        return ans