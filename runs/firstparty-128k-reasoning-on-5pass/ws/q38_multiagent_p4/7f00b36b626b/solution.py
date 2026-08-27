from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        t = threshold

        # present[x] is used only for x <= threshold.
        present = [False] * (t + 1)
        small = []

        # Initial component count.
        # Under the stated uniqueness constraint this equals len(nums).
        # Counting unique small values also keeps the code correct if duplicates appear.
        components = 0
        for x in nums:
            if x > t:
                # Any value > threshold is isolated because lcm(a, b) >= max(a, b).
                components += 1
            elif not present[x]:
                present[x] = True
                small.append(x)
                components += 1

        if not small:
            return components

        parent = list(range(t + 1))
        rank = [0] * (t + 1)

        def find(a: int) -> int:
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a: int, b: int) -> bool:
            ra = find(a)
            rb = find(b)
            if ra == rb:
                return False

            if rank[ra] < rank[rb]:
                ra, rb = rb, ra

            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1
            return True

        # first[m] stores the first present divisor of m seen so far.
        first = [0] * (t + 1)

        for x in small:
            for m in range(x, t + 1, x):
                rep = first[m]
                if rep == 0:
                    first[m] = x
                else:
                    # x and rep both divide m, so lcm(x, rep) <= m <= threshold.
                    if union(x, rep):
                        components -= 1

        return components


if __name__ == "__main__":
    import math
    import random

    sol = Solution()

    # Given examples.
    assert sol.countComponents([2, 4, 8, 3, 9], 5) == 4
    assert sol.countComponents([2, 4, 8, 3, 9, 12], 10) == 2

    def brute_force(nums: List[int], threshold: int) -> int:
        n = len(nums)
        parent = list(range(n))

        def find(a: int) -> int:
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a: int, b: int) -> bool:
            ra = find(a)
            rb = find(b)
            if ra == rb:
                return False
            parent[rb] = ra
            return True

        comps = n
        for i in range(n):
            for j in range(i + 1, n):
                a = nums[i]
                b = nums[j]
                g = math.gcd(a, b)
                if (a // g) * b <= threshold and union(i, j):
                    comps -= 1
        return comps

    random.seed(12345)

    # Randomized unique-value tests, matching the problem constraints.
    for _ in range(300):
        t = random.randint(1, 40)
        n = random.randint(1, 12)
        max_val = max(t + 10, 12)
        nums = random.sample(range(1, max_val + 1), n)
        assert sol.countComponents(nums, t) == brute_force(nums, t)

    # Extra duplicate-value tests for robustness.
    for _ in range(100):
        t = random.randint(1, 30)
        n = random.randint(1, 10)
        nums = [random.randint(1, t + 5) for _ in range(n)]
        assert sol.countComponents(nums, t) == brute_force(nums, t)