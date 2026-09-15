from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        T = threshold

        # Values > T can never form an edge: lcm(a, b) >= max(a, b) > T.
        small = [v for v in nums if v <= T]
        big = len(nums) - len(small)

        idx = {v: i for i, v in enumerate(small)}
        n = len(small)
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

        # last[m] = most recent present divisor of m seen so far (0 = none).
        # lcm(a, b) <= T  <=>  both a and b divide some m <= T.
        last = [0] * (T + 1)
        for v in small:
            iv = idx[v]
            for m in range(v, T + 1, v):
                if last[m]:
                    union(iv, idx[last[m]])
                last[m] = v

        roots = set()
        for v in small:
            roots.add(find(idx[v]))

        return len(roots) + big