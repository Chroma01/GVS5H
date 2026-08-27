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

        def union(a: int, b: int) -> None:
            ra = find(a)
            rb = find(b)
            if ra == rb:
                return
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]

        index = {value: i for i, value in enumerate(nums)}
        representative = [-1] * (threshold + 1)

        for value in nums:
            if value > threshold:
                continue

            current = index[value]
            for multiple in range(value, threshold + 1, value):
                previous = representative[multiple]
                if previous != -1:
                    union(current, previous)
                representative[multiple] = current

        return len({find(i) for i in range(n)})