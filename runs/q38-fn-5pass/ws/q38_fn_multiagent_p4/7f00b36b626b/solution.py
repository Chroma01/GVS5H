from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        small = [x for x in nums if x <= threshold]
        isolated = len(nums) - len(small)

        if not small:
            return isolated

        # Processing smaller values first makes first[multiple] usually the
        # smallest present divisor, which improves DSU path behavior.
        small.sort()

        parent = list(range(threshold + 1))
        size = [1] * (threshold + 1)
        first = [0] * (threshold + 1)  # first[L] = first present divisor of L seen

        def find(x: int, parent=parent) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        components = len(small)
        limit = threshold + 1

        for a in small:
            root_a = find(a)

            for multiple in range(a, limit, a):
                seen = first[multiple]

                if seen:
                    # If the stored divisor is already the current root,
                    # this multiple is already in a's component.
                    if seen == root_a:
                        continue

                    root_seen = find(seen)

                    if root_a != root_seen:
                        # Union by size. On ties, attach root_a under root_seen
                        # so root_a often becomes the existing representative.
                        if size[root_a] < size[root_seen]:
                            parent[root_a] = root_seen
                            size[root_seen] += size[root_a]
                            root_a = root_seen
                        elif size[root_a] > size[root_seen]:
                            parent[root_seen] = root_a
                            size[root_a] += size[root_seen]
                        else:
                            parent[root_a] = root_seen
                            size[root_seen] += size[root_a]
                            root_a = root_seen

                        components -= 1
                else:
                    first[multiple] = a

        return components + isolated


if __name__ == "__main__":
    sol = Solution()
    assert sol.countComponents([2, 4, 8, 3, 9], 5) == 4
    assert sol.countComponents([2, 4, 8, 3, 9, 12], 10) == 2
    print("All sample tests passed")