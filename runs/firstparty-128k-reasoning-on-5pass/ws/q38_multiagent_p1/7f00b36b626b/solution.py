from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        present = [False] * (threshold + 1)
        isolated = 0
        small_count = 0

        for x in nums:
            if x <= threshold:
                if not present[x]:
                    present[x] = True
                    small_count += 1
            else:
                isolated += 1

        if small_count == 0:
            return isolated

        parent = list(range(threshold + 1))
        size = [1] * (threshold + 1)

        def find(a: int) -> int:
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        first_rep = [0] * (threshold + 1)

        for x in range(1, threshold + 1):
            if not present[x]:
                continue

            root_x = find(x)
            for m in range(x, threshold + 1, x):
                rep = first_rep[m]
                if rep == 0:
                    first_rep[m] = x
                elif rep != x:
                    if rep != root_x:
                        rrep = find(rep)
                        if rrep != root_x:
                            if size[root_x] <= size[rrep]:
                                parent[root_x] = rrep
                                size[rrep] += size[root_x]
                                root_x = rrep
                            else:
                                parent[rrep] = root_x
                                size[root_x] += size[rrep]

        roots = set()
        for x in range(1, threshold + 1):
            if present[x]:
                roots.add(find(x))

        return len(roots) + isolated


if __name__ == "__main__":
    sol = Solution()

    assert sol.countComponents([2, 4, 8, 3, 9], 5) == 4
    assert sol.countComponents([2, 4, 8, 3, 9, 12], 10) == 2

    assert sol.countComponents([1], 1) == 1
    assert sol.countComponents([1, 2], 1) == 2
    assert sol.countComponents([10, 20, 30], 5) == 3
    assert sol.countComponents([1, 2, 3, 4, 5], 5) == 1
    assert sol.countComponents([4, 6, 12], 12) == 1
    assert sol.countComponents([4, 6, 12], 11) == 3

    import time
    big = list(range(1, 100001))
    t0 = time.perf_counter()
    assert sol.countComponents(big, 200000) == 1
    t1 = time.perf_counter()
    print(f"performance test: {t1 - t0:.3f}s")