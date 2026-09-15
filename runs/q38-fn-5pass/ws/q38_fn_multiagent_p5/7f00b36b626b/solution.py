from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        t = threshold

        # DSU nodes:
        # 0 .. n-1          : original graph nodes
        # n+1 .. n+t        : auxiliary nodes representing multiples 1..t
        # index n is unused but keeps indexing simple.
        total = n + t + 1
        parent = list(range(total))
        size = [1] * total

        def find(x: int, parent=parent) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        base = n

        for i, x in enumerate(nums):
            # If x > threshold, it cannot be connected to anything,
            # because lcm(x, y) >= x > threshold for every positive y.
            if x <= t:
                ri = find(i)

                # Connect this original node to every auxiliary node m
                # such that m is a multiple of x and m <= threshold.
                for m in range(x, t + 1, x):
                    rj = find(base + m)
                    if ri != rj:
                        if size[ri] < size[rj]:
                            ri, rj = rj, ri
                        parent[rj] = ri
                        size[ri] += size[rj]

        # Count distinct components among original nodes only.
        return len({find(i) for i in range(n)})