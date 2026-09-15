from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        T = threshold

        present = bytearray(T + 1)
        small_vals = []
        large_count = 0

        for x in nums:
            if x <= T:
                if not present[x]:
                    present[x] = 1
                    small_vals.append(x)
            else:
                large_count += 1

        # DSU over values 1..T
        parent = list(range(T + 1))
        size = [1] * (T + 1)

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

        # rep[m] = first present small value seen that divides m
        rep = [0] * (T + 1)

        for d in small_vals:
            for m in range(d, T + 1, d):
                r = rep[m]
                if r == 0:
                    rep[m] = d
                else:
                    union(r, d)

        components = large_count
        for d in small_vals:
            if find(d) == d:
                components += 1

        return components