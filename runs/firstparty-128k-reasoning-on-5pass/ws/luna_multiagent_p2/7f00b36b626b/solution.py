from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        parent = list(range(n))
        size = [1] * n
        components = n

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            nonlocal components
            ra = find(a)
            rb = find(b)

            if ra == rb:
                return

            if size[ra] < size[rb]:
                ra, rb = rb, ra

            parent[rb] = ra
            size[ra] += size[rb]
            components -= 1

        owner = [-1] * (threshold + 1)

        for index, value in enumerate(nums):
            if value > threshold:
                continue

            for multiple in range(value, threshold + 1, value):
                if owner[multiple] == -1:
                    owner[multiple] = index
                else:
                    union(index, owner[multiple])

        return components