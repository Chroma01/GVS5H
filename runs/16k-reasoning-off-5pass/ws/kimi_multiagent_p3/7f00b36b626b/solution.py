from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            # iterative path compression
            root = x
            while parent[root] != root:
                root = parent[root]
            while parent[x] != root:
                parent[x], x = root, parent[x]
            return root

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1

        # Key fact: if a | L and b | L, then lcm(a, b) | L, so lcm(a, b) <= L.
        # Hence for every L <= threshold, all present values dividing L form a
        # clique. Conversely, any edge (a, b) with lcm(a, b) = L0 <= threshold
        # is witnessed at L = L0 since both a and b divide L0.
        #
        # rep[L] = index of the first present divisor of L encountered; every
        # later present divisor of L is unioned with it, building the clique.
        #
        # Values > threshold can never have an edge (lcm(a,b) >= max(a,b)),
        # so they stay as singleton components automatically.
        rep = {}
        for i, v in enumerate(nums):
            if v > threshold:
                continue
            for L in range(v, threshold + 1, v):
                r = rep.get(L)
                if r is None:
                    rep[L] = i
                else:
                    union(i, r)

        roots = set()
        for i in range(n):
            roots.add(find(i))
        return len(roots)