import math
import random
import time
import sys
from typing import List


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        T = threshold
        large = 0
        present = []
        seen = set()

        for v in nums:
            if v > T:
                large += 1
            elif v not in seen:
                seen.add(v)
                present.append(v)

        if not present:
            return large

        parent = list(range(T + 1))
        rank = [0] * (T + 1)

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra = find(a)
            rb = find(b)
            if ra == rb:
                return
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1

        for x in present:
            for m in range(x * 2, T + 1, x):
                union(x, m)

        roots = set()
        for x in present:
            roots.add(find(x))

        return len(roots) + large


def brute(nums, threshold):
    n = len(nums)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for i in range(n):
        for j in range(i + 1, n):
            if math.lcm(nums[i], nums[j]) <= threshold:
                union(i, j)

    return len({find(i) for i in range(n)})


def main():
    sol = Solution()

    # (a) Provided examples
    ex1 = sol.countComponents([2, 4, 8, 3, 9], 5)
    ex2 = sol.countComponents([2, 4, 8, 3, 9, 12], 10)
    print(f"Example 1: got {ex1}, expected 4 -> {'PASS' if ex1 == 4 else 'FAIL'}")
    print(f"Example 2: got {ex2}, expected 2 -> {'PASS' if ex2 == 2 else 'FAIL'}")

    # Extra edge cases
    edge_cases = [
        ([1, 10**9], 5, 2),
        ([5], 5, 1),
        ([6], 5, 1),
        ([2, 3, 5], 10, 1),
        ([4, 6], 11, 2),
        ([4, 6], 12, 1),
    ]
    for nums, t, exp in edge_cases:
        got = sol.countComponents(nums, t)
        status = "PASS" if got == exp else "FAIL"
        print(f"Edge {nums} T={t}: got {got}, expected {exp} -> {status}")

    # (b) Randomized brute-force cross-check
    random.seed(12345)
    fails = 0
    for trial in range(5000):
        n = random.randint(1, 7)
        maxval = random.randint(1, 25)
        pool = random.sample(range(1, maxval + 1), min(n, maxval))
        nums = pool
        threshold = random.randint(1, 25)
        got = sol.countComponents(nums, threshold)
        exp = brute(nums, threshold)
        if got != exp:
            fails += 1
            if fails <= 10:
                print(f"MISMATCH nums={nums} T={threshold}: got {got}, brute {exp}")
    print(f"Randomized cross-check: 5000 trials, {fails} mismatches -> "
          f"{'PASS' if fails == 0 else 'FAIL'}")

    # Larger randomized with bigger values
    fails2 = 0
    for trial in range(2000):
        n = random.randint(1, 10)
        nums = random.sample(range(1, 60), n)
        threshold = random.randint(1, 60)
        got = sol.countComponents(nums, threshold)
        exp = brute(nums, threshold)
        if got != exp:
            fails2 += 1
            if fails2 <= 10:
                print(f"MISMATCH2 nums={nums} T={threshold}: got {got}, brute {exp}")
    print(f"Randomized cross-check (larger): 2000 trials, {fails2} mismatches -> "
          f"{'PASS' if fails2 == 0 else 'FAIL'}")

    # (c) Worst-case performance
    T = 2 * 10**5
    nums = list(range(1, 10**5 + 1))  # distinct 1..1e5, all <= T
    start = time.time()
    res = sol.countComponents(nums, T)
    elapsed = time.time() - start
    print(f"Performance: nums=1..100000, T={T}: result={res}, time={elapsed:.3f}s")


if __name__ == "__main__":
    main()