from typing import List

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.count -= 1
        return True

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        # Map value to index for O(1) lookup
        pos = {v: i for i, v in enumerate(nums)}
        uf = UnionFind(n)
        
        # For each element, find multiples in array that are <= threshold
        for i, a in enumerate(nums):
            if a > threshold:
                # No edges possible for this element (isolated)
                continue
            # Iterate multiples of a: a, 2a, 3a, ... up to threshold
            m = a
            while m <= threshold:
                if m in pos and pos[m] != i:
                    uf.union(i, pos[m])
                m += a
                # Avoid infinite loop if a == 0 (not possible per constraints)
                if a == 0:
                    break
        
        return uf.count