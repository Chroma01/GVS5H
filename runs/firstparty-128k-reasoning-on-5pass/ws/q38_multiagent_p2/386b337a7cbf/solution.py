from typing import List
import random
import sys

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        total = sum(nums)
        if abs(k) > total:
            return -1

        off = total
        mask = (1 << (2 * total + 1)) - 1

        all_even = 0
        all_odd = 0

        dp_even = [0] * (limit + 1)
        dp_odd = [0] * (limit + 1)

        for x in nums:
            if x > 0:
                old_all_even, old_all_odd = all_even, all_odd
                old_dp_even, old_dp_odd = dp_even, dp_odd

                dp_even = dp_even.copy()
                dp_odd = dp_odd.copy()

                all_even = (old_all_even | (old_all_odd >> x)) & mask
                all_odd = (old_all_odd | (old_all_even << x)) & mask
                all_odd |= 1 << (off + x)

                dp_even[0] |= old_dp_odd[0] >> x
                dp_odd[0] |= (old_dp_even[0] << x) & mask

                if x <= limit:
                    dp_odd[x] |= 1 << (off + x)
                    for p in range(1, limit // x + 1):
                        bits = old_dp_odd[p]
                        if bits:
                            dp_even[p * x] |= bits >> x
                        bits = old_dp_even[p]
                        if bits:
                            dp_odd[p * x] |= (bits << x) & mask
            else:
                old_all_even, old_all_odd = all_even, all_odd

                dp_even[0] |= old_all_odd
                dp_odd[0] |= old_all_even
                dp_odd[0] |= 1 << off

                all_even = (old_all_even | old_all_odd) & mask
                all_odd = (old_all_odd | old_all_even) & mask
                all_odd |= 1 << off

        target = 1 << (off + k)

        for p in range(limit, 0, -1):
            if (dp_even[p] & target) or (dp_odd[p] & target):
                return p

        if (dp_even[0] & target) or (dp_odd[0] & target):
            return 0

        return -1


def brute_force(nums: List[int], k: int, limit: int) -> int:
    n = len(nums)
    best = -1
    for mask in range(1, 1 << n):
        prod = 1
        asum = 0
        idx = 0
        for i, v in enumerate(nums):
            if mask & (1 << i):
                if idx % 2 == 0:
                    asum += v
                else:
                    asum -= v
                idx += 1
                prod *= v
        if asum == k and prod <= limit:
            if prod > best:
                best = prod
    return best


def run_verification() -> bool:
    sol = Solution()

    examples = [
        ([1, 2, 3], 2, 10, 6),
        ([0, 2, 3], -5, 12, -1),
        ([2, 2, 3, 3], 0, 9, 9),
    ]
    for nums, k, limit, expected in examples:
        bf = brute_force(nums, k, limit)
        if bf != expected:
            print(f"Example brute mismatch: nums={nums}, k={k}, limit={limit}, expected={expected}, brute={bf}")
            return False
        got = sol.maxProduct(nums, k, limit)
        if got != expected:
            print(f"Example failed: nums={nums}, k={k}, limit={limit}, expected={expected}, got={got}")
            return False

    edge_cases = [
        ([0], 0, 1, 0),
        ([0], 1, 1, -1),
        ([1], 1, 1, 1),
        ([2], 2, 1, -1),
        ([2, 2], 0, 3, -1),
        ([2, 2], 0, 4, 4),
        ([0, 1], -1, 1, 0),
        ([1, 0], 1, 1, 1),
        ([1, 1, 1], 0, 1, 1),
        ([1, 1, 1], 1, 1, 1),
        ([1, 1, 1], -1, 1, -1),
        ([5, 0, 5], 0, 4, 0),
        ([5, 0, 5], -5, 4, 0),
        ([0, 5, 5], 0, 4, 0),
        ([1] * 150, 0, 5000, 1),
        ([1] * 150, 1, 5000, 1),
        ([1] * 150, 2, 5000, -1),
        ([0] * 150, 0, 1, 0),
        ([0] * 150, 1, 1, -1),
    ]
    for nums, k, limit, expected in edge_cases:
        if len(nums) <= 10:
            bf = brute_force(nums, k, limit)
            if bf != expected:
                print(f"Edge brute mismatch: nums={nums}, k={k}, limit={limit}, expected={expected}, brute={bf}")
                return False
        got = sol.maxProduct(nums, k, limit)
        if got != expected:
            print(f"Edge failed: n={len(nums)}, k={k}, limit={limit}, expected={expected}, got={got}")
            return False

    random.seed(12345)
    for _ in range(3000):
        n = random.randint(1, 8)
        max_val = random.choice([2, 3, 4, 6, 12])
        nums = [random.randint(0, max_val) for _ in range(n)]
        total = sum(nums)
        limit = random.randint(1, 30)
        if random.random() < 0.2:
            k = random.randint(-total - 3, total + 3)
        else:
            k = random.randint(-total, total)
        expected = brute_force(nums, k, limit)
        got = sol.maxProduct(nums, k, limit)
        if got != expected:
            print(f"Random failed: nums={nums}, k={k}, limit={limit}, expected={expected}, got={got}")
            return False

    for _ in range(500):
        n = random.randint(1, 5)
        nums = [random.randint(0, 3) for _ in range(n)]
        total = sum(nums)
        limit = random.randint(1, 12)
        for k in range(-total, total + 1):
            expected = brute_force(nums, k, limit)
            got = sol.maxProduct(nums, k, limit)
            if got != expected:
                print(f"Small all-k failed: nums={nums}, k={k}, limit={limit}, expected={expected}, got={got}")
                return False

    print("All verification tests passed")
    return True


if __name__ == "__main__":
    sys.exit(0 if run_verification() else 1)