from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        T = threshold
        present = [False] * (T + 1)
        small = []
        isolated = 0

        for v in nums:
            if v > T:
                isolated += 1
            elif not present[v]:
                present[v] = True
                small.append(v)

        if len(small) <= 1:
            return len(small) + isolated

        parent = list(range(T + 1))
        size = [1] * (T + 1)
        last = [0] * (T + 1)
        components = len(small)

        for x in small:
            rx = x
            while parent[rx] != rx:
                parent[rx] = parent[parent[rx]]
                rx = parent[rx]

            for m in range(x, T + 1, x):
                y = last[m]
                if y:
                    ry = y
                    while parent[ry] != ry:
                        parent[ry] = parent[parent[ry]]
                        ry = parent[ry]

                    if rx != ry:
                        if size[rx] < size[ry]:
                            parent[rx] = ry
                            size[ry] += size[rx]
                            rx = ry
                        else:
                            parent[ry] = rx
                            size[rx] += size[ry]
                        components -= 1

                last[m] = x

        return components + isolated


def _run_sample_tests() -> None:
    sol = Solution()
    tests = [
        ([2, 4, 8, 3, 9], 5, 4),
        ([2, 4, 8, 3, 9, 12], 10, 2),
        ([10, 20, 30], 5, 3),
        ([1, 2, 3], 1, 3),
        ([1], 1, 1),
        ([1, 2, 3, 4], 4, 1),
        ([1, 200000], 200000, 1),
        ([199999, 200000], 200000, 2),
        ([5, 7], 10, 2),
        ([10, 5], 10, 1),
    ]

    all_pass = True
    for nums, threshold, expected in tests:
        actual = sol.countComponents(nums, threshold)
        passed = actual == expected
        all_pass = all_pass and passed
        print(f"nums={nums} threshold={threshold} expected={expected} actual={actual} {'PASS' if passed else 'FAIL'}")

    print(f"verdict={'PASS' if all_pass else 'FAIL'}")


if __name__ == "__main__":
    _run_sample_tests()