from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        parent = list(range(threshold + 1))
        size = [1] * (threshold + 1)

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

        active = []
        isolated = 0

        for value in nums:
            if value <= threshold:
                active.append(value)
            else:
                isolated += 1

        for value in active:
            for multiple in range(value, threshold + 1, value):
                union(value, multiple)

        return len({find(value) for value in active}) + isolated