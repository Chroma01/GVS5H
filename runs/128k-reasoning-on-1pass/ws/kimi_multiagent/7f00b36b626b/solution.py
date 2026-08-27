from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        T = threshold

        small = []
        large_count = 0
        for x in nums:
            if x <= T:
                small.append(x)
            else:
                large_count += 1

        m = len(small)
        parent = list(range(m))
        size = [1] * m

        def find(a: int) -> int:
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]

        # first[L] = index of the first present value that divides L
        first = [-1] * (T + 1)

        for idx, x in enumerate(small):
            for multiple in range(x, T + 1, x):
                rep = first[multiple]
                if rep == -1:
                    first[multiple] = idx
                else:
                    union(idx, rep)

        components = 0
        for i in range(m):
            if find(i) == i:
                components += 1

        return components + large_count