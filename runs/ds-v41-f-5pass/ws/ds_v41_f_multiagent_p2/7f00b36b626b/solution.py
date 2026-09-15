from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # Values greater than threshold can never be in an edge (lcm(a,b) >= max(a,b)).
        active = [v for v in nums if v <= threshold]
        isolated = len(nums) - len(active)
        if not active:
            return isolated

        # Map each distinct active value to a DSU index.
        idx = {}
        for v in active:
            if v not in idx:
                idx[v] = len(idx)
        n = len(idx)

        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        # first_divisor[L] = index of the first active value found dividing L.
        first_divisor = [-1] * (threshold + 1)

        for v in active:
            i = idx[v]
            for L in range(v, threshold + 1, v):
                j = first_divisor[L]
                if j == -1:
                    first_divisor[L] = i
                else:
                    union(i, j)

        roots = set()
        for i in range(n):
            roots.add(find(i))

        return len(roots) + isolated