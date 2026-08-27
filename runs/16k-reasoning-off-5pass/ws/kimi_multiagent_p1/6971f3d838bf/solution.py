from typing import List
from collections import defaultdict


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        NEG_INF = float('-inf')

        size = 1
        while size < n:
            size <<= 1

        # Node: (total, best_prefix, best_suffix, best_subarray)
        tree = [(0, NEG_INF, NEG_INF, NEG_INF)] * (2 * size)

        def combine(a, b):
            total = a[0] + b[0]
            pref = a[1] if a[1] > a[0] + b[1] else a[0] + b[1]
            suff = b[2] if b[2] > b[0] + a[2] else b[0] + a[2]
            best = a[3] if a[3] > b[3] else b[3]
            cross = a[2] + b[1]
            if cross > best:
                best = cross
            return (total, pref, suff, best)

        for i, v in enumerate(nums):
            tree[size + i] = (v, v, v, v)
        for i in range(size - 1, 0, -1):
            tree[i] = combine(tree[2 * i], tree[2 * i + 1])

        IDENTITY = (0, NEG_INF, NEG_INF, NEG_INF)

        def query_node(l, r):
            """Return merged node over nums[l..r] inclusive (l <= r)."""
            l += size
            r += size
            left_res = IDENTITY
            right_res = IDENTITY
            while l <= r:
                if l & 1:
                    left_res = combine(left_res, tree[l])
                    l += 1
                if not (r & 1):
                    right_res = combine(tree[r], right_res)
                    r -= 1
                l >>= 1
                r >>= 1
            return combine(left_res, right_res)

        # Case 1: no deletion
        ans = query_node(0, n - 1)[3]

        # Group indices by value
        positions = defaultdict(list)
        for i, v in enumerate(nums):
            positions[v].append(i)

        # Case 2: delete all occurrences of x. The remaining gaps become
        # adjacent, so merge gap nodes in order and take the best field.
        for x, idxs in positions.items():
            if len(idxs) == n:
                continue  # deletion would empty the array
            merged = IDENTITY
            prev = -1
            for idx in idxs:
                if idx - 1 >= prev + 1:
                    merged = combine(merged, query_node(prev + 1, idx - 1))
                prev = idx
            if prev + 1 <= n - 1:
                merged = combine(merged, query_node(prev + 1, n - 1))
            if merged[3] > ans:
                ans = merged[3]

        return ans