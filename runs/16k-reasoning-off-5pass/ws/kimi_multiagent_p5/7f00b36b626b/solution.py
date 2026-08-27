from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        parent = list(range(n))
        rank = [0] * n

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

        # Map value -> index for values that can possibly have an edge (value <= threshold)
        idx_of = {}
        for i, v in enumerate(nums):
            if v <= threshold:
                idx_of[v] = i

        # For each possible gcd d, connect the smallest present multiple s of d
        # with every other present multiple m where lcm(s, m) = s*m/d <= threshold.
        for d in range(1, threshold + 1):
            s = -1  # smallest present multiple of d
            for m in range(d, threshold + 1, d):
                if m in idx_of:
                    if s == -1:
                        s = m
                    else:
                        # lcm(s, m) = s*m/d (exact since d divides both)
                        if s * m // d <= threshold:
                            union(idx_of[s], idx_of[m])
                        else:
                            # m increases, so s*m/d only grows; safe to stop
                            break

        roots = set()
        for i in range(n):
            roots.add(find(i))
        return len(roots)