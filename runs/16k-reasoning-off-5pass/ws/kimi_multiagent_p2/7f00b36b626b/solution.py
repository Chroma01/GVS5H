from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        T = threshold

        # DSU over values 1..T
        parent = list(range(T + 1))
        rank = [0] * (T + 1)

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1

        present = [False] * (T + 1)
        big = 0  # values > threshold: always isolated
        for v in nums:
            if v > T:
                big += 1
            else:
                present[v] = True

        # divisors[L] = list of present values that divide L
        # built by iterating multiples of each present value
        divisors = [[] for _ in range(T + 1)]
        for v in range(1, T + 1):
            if present[v]:
                for m in range(v, T + 1, v):
                    divisors[m].append(v)

        # For each L, all present divisors of L pairwise have lcm dividing L,
        # hence lcm <= T, so they are all mutually connected.
        for L in range(1, T + 1):
            lst = divisors[L]
            if len(lst) >= 2:
                first = lst[0]
                for other in lst[1:]:
                    union(first, other)

        roots = set()
        for v in range(1, T + 1):
            if present[v]:
                roots.add(find(v))

        return len(roots) + big