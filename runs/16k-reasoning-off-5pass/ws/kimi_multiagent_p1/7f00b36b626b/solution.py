from typing import List
from math import gcd


class DSU:
    __slots__ = ("parent", "rank")

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        parent = self.parent
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        dsu = DSU(n)

        # Map value -> node index for values that can possibly have an edge.
        # Since lcm(a, b) >= max(a, b), any value > threshold is isolated.
        idx_of = [-1] * (threshold + 1)
        for i, v in enumerate(nums):
            if v <= threshold:
                idx_of[v] = i

        # For each present value v, check its multiples m <= threshold.
        # lcm(v, m) = v * m / gcd(v, m); union when it fits in threshold.
        for v in range(1, threshold + 1):
            iv = idx_of[v]
            if iv == -1:
                continue
            for m in range(2 * v, threshold + 1, v):
                im = idx_of[m]
                if im != -1 and (v // gcd(v, m)) * m <= threshold:
                    dsu.union(iv, im)

        # Count distinct roots over ALL nodes (isolated big values included).
        roots = set()
        for i in range(n):
            roots.add(dsu.find(i))
        return len(roots)