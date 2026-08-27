from typing import List
from collections import defaultdict

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)

        # Node = (total sum, max nonempty prefix sum, max nonempty suffix sum, max subarray sum)
        # combine(a, b) returns the node for the concatenation of segments a then b.
        def combine(a, b):
            s = a[0] + b[0]
            pref = a[1] if a[1] > a[0] + b[1] else a[0] + b[1]
            suff = b[2] if b[2] > b[0] + a[2] else b[0] + a[2]
            best = a[3] if a[3] > b[3] else b[3]
            cross = a[2] + b[1]
            if cross > best:
                best = cross
            return (s, pref, suff, best)

        # Iterative segment tree over the array (works for any n, half-open queries).
        tree = [None] * (2 * n)
        for i in range(n):
            v = nums[i]
            tree[n + i] = (v, v, v, v)
        for i in range(n - 1, 0, -1):
            tree[i] = combine(tree[2 * i], tree[2 * i + 1])

        def query(l: int, r: int):
            # max-subarray node for nums[l..r] inclusive
            l += n
            r += n + 1
            left_res = None
            right_res = None
            while l < r:
                if l & 1:
                    left_res = tree[l] if left_res is None else combine(left_res, tree[l])
                    l += 1
                if r & 1:
                    r -= 1
                    right_res = tree[r] if right_res is None else combine(tree[r], right_res)
                l >>= 1
                r >>= 1
            if left_res is None:
                return right_res
            if right_res is None:
                return left_res
            return combine(left_res, right_res)

        # Prefix / suffix fold nodes: pre[i] = fold of nums[0..i], suf[i] = fold of nums[i..n-1]
        pre = [None] * n
        suf = [None] * n
        cur = None
        for i in range(n):
            node = (nums[i], nums[i], nums[i], nums[i])
            cur = node if cur is None else combine(cur, node)
            pre[i] = cur
        cur = None
        for i in range(n - 1, -1, -1):
            node = (nums[i], nums[i], nums[i], nums[i])
            cur = node if cur is None else combine(node, cur)
            suf[i] = cur

        # Group occurrence positions by value.
        pos = defaultdict(list)
        for i, v in enumerate(nums):
            pos[v].append(i)

        # No-operation answer: Kadane over the whole array.
        ans = pre[n - 1][3]

        # For each value x, the array after deleting all x's is the concatenation of the
        # gaps between consecutive occurrences of x. Fold the gap nodes with combine.
        for v, ps in pos.items():
            k = len(ps)
            if k == n:
                continue  # deletion would empty the array -> not allowed
            cur = None
            if ps[0] > 0:  # left end gap nums[0..ps[0]-1]
                cur = pre[ps[0] - 1]
            for i in range(k - 1):  # internal gaps between consecutive occurrences
                a = ps[i] + 1
                b = ps[i + 1] - 1
                if a <= b:
                    node = query(a, b)
                    cur = node if cur is None else combine(cur, node)
            if ps[-1] < n - 1:  # right end gap nums[ps[-1]+1..n-1]
                node = suf[ps[-1] + 1]
                cur = node if cur is None else combine(cur, node)
            if cur is not None and cur[3] > ans:
                ans = cur[3]

        return ans