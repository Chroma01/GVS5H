from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # Only values <= threshold can be incident to any edge.
        active = [x for x in nums if x <= threshold]
        if not active:
            return len(nums)

        parent = list(range(threshold + 1))
        rank = [0] * (threshold + 1)

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> bool:
            ra = find(a)
            rb = find(b)
            if ra == rb:
                return False
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1
            return True

        # rep[m] stores one active divisor of m, if any has been seen.
        rep = [0] * (threshold + 1)
        unions = 0
        t = threshold

        for d in active:
            for m in range(d, t + 1, d):
                r = rep[m]
                if r == 0:
                    rep[m] = d
                elif r != d:
                    if union(d, r):
                        unions += 1

        return len(nums) - unions