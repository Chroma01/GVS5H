from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # DSU over values 1..threshold (only values present in nums are real nodes)
        parent = list(range(threshold + 1))
        rank = [0] * (threshold + 1)

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

        present = [False] * (threshold + 1)
        big = 0  # values > threshold are isolated nodes
        for v in nums:
            if v > threshold:
                big += 1
            else:
                present[v] = True

        # anchor[L] = a present divisor of L used as the representative for L.
        # For every present v, for each multiple L of v, all present divisors of L
        # get unioned together. This is valid because lcm of any two divisors of L
        # divides L, hence is <= threshold. It is complete because any edge (a,b)
        # with lcm(a,b) = L0 <= threshold is captured when processing L = L0.
        anchor = [-1] * (threshold + 1)
        for v in nums:
            if v > threshold:
                continue
            for L in range(v, threshold + 1, v):
                a = anchor[L]
                if a == -1:
                    anchor[L] = v
                else:
                    union(v, a)

        roots = set()
        for v in nums:
            if v <= threshold:
                roots.add(find(v))

        return len(roots) + big