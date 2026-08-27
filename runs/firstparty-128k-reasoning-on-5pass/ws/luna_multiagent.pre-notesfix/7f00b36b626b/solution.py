from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        parent = list(range(n))
        size = [1] * n

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
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
            return True

        index = {value: i for i, value in enumerate(nums) if value <= threshold}

        # representative[m] stores one present value dividing m.
        representative = [-1] * (threshold + 1)
        components = n

        for value, idx in index.items():
            for multiple in range(value, threshold + 1, value):
                other = representative[multiple]
                if other == -1:
                    representative[multiple] = idx
                elif union(idx, other):
                    components -= 1

        return components