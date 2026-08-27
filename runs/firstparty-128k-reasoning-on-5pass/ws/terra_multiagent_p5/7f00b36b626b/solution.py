from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        present = []
        isolated = 0

        for x in nums:
            if x > threshold:
                isolated += 1
            else:
                present.append(x)

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

        # representative[m] is one present input value dividing m.
        # All present divisors of the same m are pairwise connected,
        # because their LCM divides m <= threshold.
        representative = [0] * (threshold + 1)

        for d in present:
            for m in range(d, threshold + 1, d):
                if representative[m] == 0:
                    representative[m] = d
                else:
                    union(d, representative[m])

        roots = set()
        for x in present:
            roots.add(find(x))

        return isolated + len(roots)