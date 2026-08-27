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

        valid_values = []
        isolated = 0

        for x in nums:
            if x > threshold:
                isolated += 1
            else:
                valid_values.append(x)

        first = [0] * (threshold + 1)

        for d in valid_values:
            for m in range(d, threshold + 1, d):
                if first[m] == 0:
                    first[m] = d
                else:
                    union(d, first[m])

        roots = set()
        for x in valid_values:
            roots.add(find(x))

        return isolated + len(roots)