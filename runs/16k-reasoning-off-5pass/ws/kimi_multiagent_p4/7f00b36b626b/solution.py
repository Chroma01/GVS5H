from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # Values > threshold can never have an edge:
        # lcm(a, b) >= max(a, b) > threshold for any partner b.
        index_of = {}
        big = 0
        for i, v in enumerate(nums):
            if v > threshold:
                big += 1
            else:
                index_of[v] = i

        n = len(nums)
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        # For each possible gcd g, gather present values that are multiples of g.
        # For a = g*x, b = g*y (both multiples of g): gcd(a, b) >= g, so
        # lcm(a, b) = a*b / gcd(a,b) <= a*b / g.
        # Hence a*b <= g*threshold  ==>  lcm(a,b) <= threshold  (no gcd needed).
        # Conversely, any edge (a,b) with lcm <= threshold is discovered when
        # g = gcd(a,b), since then lcm = a*b/g <= threshold  ==>  a*b <= g*threshold.
        for g in range(1, threshold + 1):
            limit = g * threshold
            group = []
            m = g
            while m <= threshold:
                if m in index_of:
                    group.append(m)
                m += g
            k = len(group)
            if k < 2:
                continue
            # group is sorted ascending (m iterated upward).
            # For each i, union with all j > i while group[i]*group[j] <= limit.
            for i in range(k - 1):
                ai = group[i]
                idx_ai = index_of[ai]
                for j in range(i + 1, k):
                    aj = group[j]
                    if ai * aj > limit:
                        break
                    union(idx_ai, index_of[aj])

        roots = set()
        for i in index_of.values():
            roots.add(find(i))
        return len(roots) + big