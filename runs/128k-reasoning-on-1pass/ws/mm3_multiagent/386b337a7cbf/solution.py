from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        max_sum = sum(nums)
        offset = max_sum
        size = max_sum * 2 + 1
        mask = (1 << size) - 1
        over = limit + 1                     # sentinel index for product > limit

        # dp[parity][product_index] -> bitset of reachable alternating sums
        dp = [[0] * (limit + 2) for _ in range(2)]   # product indices 0..limit, over = limit+1

        for a in nums:
            # keep a copy of the current dp (states not using a)
            old = [row[:] for row in dp]

            # base case: subsequence consisting only of a (length 1, odd)
            if a <= limit:
                prod_idx = a
            else:
                prod_idx = over
            dp[1][prod_idx] |= (1 << (offset + a))

            # extend all existing non‑empty subsequences
            for parity in (0, 1):
                old_row = old[parity]
                new_parity = 1 - parity
                for prod_idx, bits in enumerate(old_row):
                    if bits == 0:
                        continue

                    # compute resulting product index
                    if a == 0:
                        new_prod_idx = 0
                    else:
                        if prod_idx == over:
                            new_prod_idx = over
                        else:
                            new_prod = prod_idx * a
                            if new_prod > limit:
                                new_prod_idx = over
                            else:
                                new_prod_idx = new_prod

                    # shift the alternating sum according to the sign of the new element
                    if parity == 0:       # even length -> new element at even index -> +a
                        shifted = (bits << a) & mask
                    else:                 # odd length -> new element at odd index -> -a
                        shifted = bits >> a

                    dp[new_parity][new_prod_idx] |= shifted

        target = offset + k
        if not (0 <= target < size):
            return -1

        ans = -1
        for parity in (0, 1):
            row = dp[parity]
            for prod in range(limit + 1):
                if (row[prod] >> target) & 1:
                    if prod > ans:
                        ans = prod
        return ans


# ------------------------------ testing harness ------------------------------
def brute_max_product(nums: List[int], k: int, limit: int) -> int:
    """Brute force solution for tiny inputs (n ≤ ~20)."""
    n = len(nums)
    best = -1
    for mask in range(1, 1 << n):
        product = 1
        sum_val = 0
        length = 0
        for i in range(n):
            if mask >> i & 1:
                if nums[i] == 0:
                    product = 0
                else:
                    product *= nums[i]
                if length % 2 == 0:
                    sum_val += nums[i]
                else:
                    sum_val -= nums[i]
                length += 1
        if sum_val == k and product <= limit:
            if product > best:
                best = product
    return best


def test_examples():
    sol = Solution()
    examples = [
        ([1, 2, 3], 2, 10, 6),
        ([0, 2, 3], -5, 12, -1),
        ([2, 2, 3, 3], 0, 9, 9),
    ]
    for nums, k, limit, expected in examples:
        res = sol.maxProduct(nums, k, limit)
        print(f"nums={nums}, k={k}, limit={limit} -> {res} (expected {expected})")
        assert res == expected, f"Failed: {nums}, {k}, {limit} got {res} expected {expected}"


def random_tests(num_tests: int = 2000):
    import random
    sol = Solution()
    for _ in range(num_tests):
        n = random.randint(1, 9)
        nums = [random.randint(0, 5) for _ in range(n)]
        max_sum = sum(nums)
        k = random.randint(-max_sum, max_sum)
        limit = random.randint(1, 20)
        dp_res = sol.maxProduct(nums, k, limit)
        brute_res = brute_max_product(nums, k, limit)
        if dp_res != brute_res:
            print("Mismatch!")
            print("nums:", nums)
            print("k:", k)
            print("limit:", limit)
            print("DP result:", dp_res)
            print("Brute result:", brute_res)
            return False
    print(f"All {num_tests} random tests passed.")
    return True


if __name__ == "__main__":
    test_examples()
    random_tests()