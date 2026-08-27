from typing import List

class DSU:
    """Disjoint Set Union with path compression and union by size."""
    __slots__ = ('parent', 'size')

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        """Return the root of x with iterative path compression."""
        parent = self.parent
        # Halve the path on the way up (loop‑based compression)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        """Merge the sets containing a and b using size heuristic."""
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return
        # Ensure ra is the larger (or equal) set
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        dsu = DSU(n)

        # first[L] stores the index of the first number that visited multiple L
        # (L ranges from 1 to threshold inclusive)
        first = [-1] * (threshold + 1)

        for idx, val in enumerate(nums):
            if val > threshold:
                # Values larger than the threshold can never share a multiple ≤ threshold
                continue
            # Enumerate all multiples of val not exceeding threshold
            for mult in range(val, threshold + 1, val):
                owner = first[mult]
                if owner == -1:
                    first[mult] = idx
                else:
                    dsu.union(idx, owner)

        # Count distinct roots among all n nodes
        roots = set()
        for i in range(n):
            roots.add(dsu.find(i))
        return len(roots)