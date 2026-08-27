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
        if n == 0:
            return 0
        
        # Map value -> index
        val_to_idx = {}
        for i, v in enumerate(nums):
            val_to_idx[v] = i
        
        dsu = DSU(n)
        
        # For each v <= threshold, find its multiples m <= threshold present in nums
        # Since lcm(v, m) = m when m is a multiple of v
        # We process each value once
        for v, idx in val_to_idx.items():
            if v > threshold:
                continue
            # Check multiples: 2*v, 3*v, ... <= threshold
            mult = 2 * v
            while mult <= threshold:
                if mult in val_to_idx:
                    dsu.union(idx, val_to_idx[mult])
                mult += v
        
        # Count unique parents
        parents = set()
        for i in range(n):
            parents.add(dsu.find(i))
        
        return len(parents)