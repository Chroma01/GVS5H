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

        index = [-1] * (threshold + 1)
        for i, value in enumerate(nums):
            if value <= threshold:
                index[value] = i

        representative = [-1] * (threshold + 1)

        for value in nums:
            if value > threshold:
                continue

            node = index[value]
            for multiple in range(value, threshold + 1, value):
                other = representative[multiple]
                if other == -1:
                    representative[multiple] = node
                else:
                    union(node, other)

        return components