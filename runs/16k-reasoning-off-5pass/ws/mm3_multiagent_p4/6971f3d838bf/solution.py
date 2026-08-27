from typing import List

class Node:
    __slots__ = ('sum', 'pref', 'suff', 'best')
    def __init__(self, sum=0, pref=0, suff=0, best=0):
        self.sum = sum
        self.pref = pref
        self.suff = suff
        self.best = best
    @staticmethod
    def combine(left, right):
        res = Node()
        res.sum = left.sum + right.sum
        res.pref = max(left.pref, left.sum + right.pref)
        res.suff = max(right.suff, right.sum + left.suff)
        res.best = max(left.best, right.best, left.suff + right.pref)
        return res

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.data = [Node() for _ in range(2 * self.size)]
        # Build leaves
        for i in range(self.n):
            self.data[self.size + i] = Node(arr[i], arr[i], arr[i], arr[i])
        for i in range(self.size - 1, 0, -1):
            self.data[i] = Node.combine(self.data[2*i], self.data[2*i+1])
    def update(self, idx, value):
        i = self.size + idx
        self.data[i] = Node(value, value, value, value)
        i //= 2
        while i:
            self.data[i] = Node.combine(self.data[2*i], self.data[2*i+1])
            i //= 2
    def query(self):
        return self.data[1].best

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        # Build segment tree
        seg = SegTree(nums)
        original_best = seg.query()
        ans = original_best
        # Build map from value to indices
        val_to_indices = {}
        for i, v in enumerate(nums):
            val_to_indices.setdefault(v, []).append(i)
        # For each unique value
        for v, indices in val_to_indices.items():
            if len(indices) == n:
                # Removing this would empty the array
                continue
            # Set to 0
            for i in indices:
                seg.update(i, 0)
            current_best = seg.query()
            if current_best > ans:
                ans = current_best
            # Revert
            for i in indices:
                seg.update(i, nums[i])
        return ans