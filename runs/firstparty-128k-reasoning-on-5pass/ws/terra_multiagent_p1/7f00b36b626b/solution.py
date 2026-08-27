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

        valid = []
        isolated = 0

        for x in nums:
            if x <= threshold:
                valid.append(x)
            else:
                isolated += 1

        representative = [0] * (threshold + 1)

        for value in valid:
            for multiple in range(value, threshold + 1, value):
                if representative[multiple] == 0:
                    representative[multiple] = value
                else:
                    union(value, representative[multiple])

        components = sum(1 for value in valid if find(value) == value)
        return components + isolated