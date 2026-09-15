from typing import List
from collections import defaultdict, Counter
import random


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)

        # Baseline: non-empty Kadane.
        best = float('-inf')
        cur = 0
        for x in nums:
            cur = x if cur + x < x else cur + x
            if cur > best:
                best = cur
        baseline = best

        # Prefix sums P[0..n].
        P = [0] * (n + 1)
        for i in range(n):
            P[i + 1] = P[i] + nums[i]

        # Segment tree over P for range max/min.
        size = 1
        while size < n + 1:
            size <<= 1
        NEG = float('-inf')
        POS = float('inf')
        tree_max = [NEG] * (2 * size)
        tree_min = [POS] * (2 * size)
        for i in range(n + 1):
            tree_max[size + i] = P[i]
            tree_min[size + i] = P[i]
        for i in range(size - 1, 0, -1):
            a = tree_max[2 * i]
            b = tree_max[2 * i + 1]
            tree_max[i] = a if a > b else b
            a = tree_min[2 * i]
            b = tree_min[2 * i + 1]
            tree_min[i] = a if a < b else b

        def qmax(l: int, r: int) -> int:
            res = NEG
            l += size
            r += size
            while l < r:
                if l & 1:
                    if tree_max[l] > res:
                        res = tree_max[l]
                    l += 1
                if r & 1:
                    r -= 1
                    if tree_max[r] > res:
                        res = tree_max[r]
                l >>= 1
                r >>= 1
            return res

        def qmin(l: int, r: int) -> int:
            res = POS
            l += size
            r += size
            while l < r:
                if l & 1:
                    if tree_min[l] < res:
                        res = tree_min[l]
                    l += 1
                if r & 1:
                    r -= 1
                    if tree_min[r] < res:
                        res = tree_min[r]
                l >>= 1
                r >>= 1
            return res

        # Occurrence indices of negative values only.
        pos_by_val = defaultdict(list)
        for i, x in enumerate(nums):
            if x < 0:
                pos_by_val[x].append(i)

        answer = baseline
        for v, occ in pos_by_val.items():
            if len(occ) >= n:
                continue  # deleting v would empty the array
            # Maximal v-free blocks [l, r).
            blocks = []
            start = 0
            for p in occ:
                if p > start:
                    blocks.append((start, p))
                start = p + 1
            if start < n:
                blocks.append((start, n))
            if len(blocks) < 2:
                continue  # any subarray lies in one original block

            cum = 0
            Q = None
            best_v = NEG
            for (l, r) in blocks:
                c = P[r] - P[l]
                pre = qmax(l + 1, r + 1) - P[l]
                suf = P[r] - qmin(l, r)
                if Q is not None:
                    cand = Q + cum + pre
                    if cand > best_v:
                        best_v = cand
                val = suf - (cum + c)
                if Q is None or val > Q:
                    Q = val
                cum += c
            if best_v > answer:
                answer = best_v

        return answer


def kadane(arr):
    best = float('-inf')
    cur = 0
    for x in arr:
        cur = x if cur + x < x else cur + x
        if cur > best:
            best = cur
    return best


def brute(nums):
    n = len(nums)
    ans = kadane(nums)
    cnt = Counter(nums)
    for x in cnt:
        if n - cnt[x] > 0:
            arr = [y for y in nums if y != x]
            val = kadane(arr)
            if val > ans:
                ans = val
    return ans


def run_tests():
    sol = Solution()

    # Provided examples.
    examples = [
        ([-3, 2, -2, -1, 3, -2, 3], 7),
        ([1, 2, 3, 4], 10),
    ]
    for nums, expected in examples:
        got = sol.maxSubarraySum(nums)
        if got != expected:
            print("FAIL")
            print("Input:", nums)
            print("Expected:", expected)
            print("Got:", got)
            return

    # Edge cases.
    edge = [
        ([5], 5),
        ([-5], -5),
        ([0], 0),
        ([-1, -1, -1], -1),
        ([2, 2, 2], 6),
        ([0, 0, 0], 0),
        ([-5, -1, -5], -1),
        ([-1, -1000, 50, -1, 50], 100),
    ]
    for nums, expected in edge:
        got = sol.maxSubarraySum(nums)
        if got != expected:
            print("FAIL")
            print("Input:", nums)
            print("Expected:", expected)
            print("Got:", got)
            return

    # Random tests.
    random.seed(12345)
    for trial in range(20000):
        n = random.randint(1, 9)
        if trial % 10 == 0:
            v = random.randint(-4, 4)
            nums = [v] * n
        elif trial % 10 == 1:
            nums = [random.randint(-4, 0) for _ in range(n)]
        else:
            nums = [random.randint(-4, 4) for _ in range(n)]

        expected = brute(nums)
        got = sol.maxSubarraySum(nums)
        if got != expected:
            print("FAIL")
            print("Input:", nums)
            print("Expected (brute):", expected)
            print("Got (solution):", got)
            return

    print("PASS")


if __name__ == "__main__":
    run_tests()