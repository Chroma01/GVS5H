from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        count = len(nums)

        # DSU over values 0..threshold. Only values <= threshold can have edges.
        parent = list(range(threshold + 1))
        size = [1] * (threshold + 1)

        # rep[m] stores the first present divisor of m seen so far.
        rep = [0] * (threshold + 1)

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        present = [x for x in nums if x <= threshold]

        for d in present:
            root_d = find(d)

            for m in range(d, threshold + 1, d):
                r = rep[m]

                if r == 0:
                    rep[m] = d
                else:
                    # Find root of r with path compression.
                    x = r
                    while parent[x] != x:
                        parent[x] = parent[parent[x]]
                        x = parent[x]

                    # Union d's component with r's component.
                    if root_d != x:
                        if size[root_d] < size[x]:
                            parent[root_d] = x
                            size[x] += size[root_d]
                            root_d = x
                        else:
                            parent[x] = root_d
                            size[root_d] += size[x]

                        count -= 1

        return count