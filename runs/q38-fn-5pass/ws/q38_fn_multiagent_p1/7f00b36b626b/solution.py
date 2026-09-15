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

        # Map each value <= threshold to its original index.
        idx_of = [-1] * (threshold + 1)
        for i, x in enumerate(nums):
            if x <= threshold:
                idx_of[x] = i

        # first[m] = index of the first present divisor of m seen so far.
        first = [-1] * (threshold + 1)

        for d in range(1, threshold + 1):
            idx = idx_of[d]
            if idx == -1:
                continue

            root_idx = find(idx)

            for m in range(d, threshold + 1, d):
                other = first[m]
                if other == -1:
                    first[m] = idx
                else:
                    root_other = find(other)
                    if root_idx != root_other:
                        if size[root_idx] < size[root_other]:
                            parent[root_idx] = root_other
                            size[root_other] += size[root_idx]
                            root_idx = root_other
                        else:
                            parent[root_other] = root_idx
                            size[root_idx] += size[root_other]
                        components -= 1

        return components