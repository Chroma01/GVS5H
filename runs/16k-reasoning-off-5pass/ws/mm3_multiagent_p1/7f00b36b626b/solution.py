from typing import List

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        # Map value -> index for values that are <= threshold.
        # Values > threshold are isolated.
        pos = {}
        for i, v in enumerate(nums):
            if v <= threshold:
                pos[v] = i
        
        uf = UnionFind(n)
        
        # For each v in 1..threshold, union it with all its multiples in the array.
        for v in range(1, threshold + 1):
            if v not in pos:
                continue
            base_idx = pos[v]
            # iterate multiples of v: 2v, 3v, ...
            multiple = 2 * v
            while multiple <= threshold:
                if multiple in pos:
                    uf.union(base_idx, pos[multiple])
                multiple += v
        
        # Count unique roots among all indices.
        roots = set()
        for i in range(n):
            roots.add(uf.find(i))
        return len(roots)