from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        present = [x for x in nums if x <= threshold]
        isolated = n - len(present)

        if not present:
            return isolated

        # Optional fast path: if 1 is present, it connects to every present value.
        if present and 1 in present:
            return 1 + isolated

        m = len(present)
        parent = list(range(m))
        rank = [0] * m

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra = find(a)
            rb = find(b)
            if ra == rb:
                return
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1

        # rep[L] is the DSU index of one present divisor of L.
        rep = [-1] * (threshold + 1)

        for idx, d in enumerate(present):
            for L in range(d, threshold + 1, d):
                r = rep[L]
                if r == -1:
                    rep[L] = idx
                else:
                    union(idx, r)

        roots = 0
        for i in range(m):
            if find(i) == i:
                roots += 1

        return roots + isolated