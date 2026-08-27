from typing import List
from collections import defaultdict

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        
        # Numbers greater than threshold are always isolated
        # because LCM(x, y) >= x > threshold
        isolated = 0
        small_indices = []  # indices of nums[i] <= threshold
        for i, v in enumerate(nums):
            if v > threshold:
                isolated += 1
            else:
                small_indices.append(i)
        
        m = len(small_indices)
        if m == 0:
            return isolated
        
        dsu = DSU(m)
        
        # Map original index -> position in small_indices
        idx_map = {orig_idx: pos for pos, orig_idx in enumerate(small_indices)}
        
        # Bucket: for each L from 1 to threshold, store positions of numbers that divide L
        buckets = defaultdict(list)
        
        for pos, orig_idx in enumerate(small_indices):
            a = nums[orig_idx]
            # Enumerate multiples of a up to threshold
            for multiple in range(a, threshold + 1, a):
                buckets[multiple].append(pos)
        
        # Union all numbers in each bucket
        for L in range(1, threshold + 1):
            group = buckets.get(L)
            if group and len(group) > 1:
                first = group[0]
                for other in group[1:]:
                    dsu.union(first, other)
        
        # Count distinct roots among small numbers
        roots = set()
        for pos in range(m):
            roots.add(dsu.find(pos))
        
        return isolated + len(roots)