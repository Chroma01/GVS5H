from typing import List
import random


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        n = len(nums)
        max_sum = 12 * n
        if abs(k) > max_sum:
            return -1

        offset = max_sum
        mask = (1 << (2 * max_sum + 1)) - 1

        # Positive-product states: no zeros, product in 1..limit.
        dp_even = [0] * (limit + 1)
        dp_odd = [0] * (limit + 1)

        # Aggregate sum DP over all non-empty subsequences.
        all_even = 0
        all_odd = 0

        # Sum DP over non-empty subsequences containing at least one zero.
        zero_even = 0
        zero_odd = 0

        zero_bit = 1 << offset
        bits = [0] * 13
        for v in range(1, 13):
            bits[v] = 1 << (offset + v)

        for x in nums:
            old_all_even = all_even
            old_all_odd = all_odd
            old_zero_even = zero_even
            old_zero_odd = zero_odd

            if x == 0:
                # Appending zero does not change the sum but toggles length parity.
                all_odd |= old_all_even
                all_even |= old_all_odd
                all_odd |= zero_bit

                # A new zero-containing subsequence is formed by appending this zero
                # to any previous non-empty subsequence, or by taking this zero alone.
                zero_odd |= old_all_even
                zero_even |= old_all_odd
                zero_odd |= zero_bit
            else:
                if x == 1:
                    # Product unchanged: snapshot each product to avoid reusing x.
                    de = dp_even
                    do = dp_odd
                    m = mask
                    for p in range(1, limit + 1):
                        oe = de[p]
                        oo = do[p]
                        if oe:
                            do[p] |= (oe << 1) & m
                        if oo:
                            de[p] |= (oo >> 1)
                    dp_odd[1] |= bits[1]
                elif x <= limit:
                    # Product increases: descending p prevents reusing the same x.
                    de = dp_even
                    do = dp_odd
                    m = mask
                    for p in range(limit // x, 0, -1):
                        oe = de[p]
                        oo = do[p]
                        if oe:
                            do[p * x] |= (oe << x) & m
                        if oo:
                            de[p * x] |= (oo >> x)
                    dp_odd[x] |= bits[x]

                # Update aggregate all-subsequence DP.
                all_odd |= (old_all_even << x) & mask
                all_even |= (old_all_odd >> x)
                all_odd |= bits[x]

                # Existing zero-containing subsequences can append x.
                zero_odd |= (old_zero_even << x) & mask
                zero_even |= (old_zero_odd >> x)

        target = 1 << (k + offset)

        # Prefer the largest positive product.
        for p in range(limit, 0, -1):
            if (dp_even[p] | dp_odd[p]) & target:
                return p

        # Fall back to product 0 if a zero-containing subsequence works.
        if (zero_even | zero_odd) & target:
            return 0

        return -1


def brute_force(nums: List[int], k: int, limit: int) -> int:
    n = len(nums)
    best = -1
    for mask in range(1, 1 << n):
        s = 0
        prod = 1
        sign = 1
        for i in range(n):
            if mask & (1 << i):
                s += sign * nums[i]
                sign = -sign
                prod *= nums[i]
        if prod <= limit and s == k:
            if prod > best:
                best = prod
    return best


def run_validation() -> None:
    sol = Solution()

    def check(nums: List[int], k: int, limit: int, expected: int | None = None) -> None:
        got = sol.maxProduct(nums, k, limit)
        if expected is None:
            expected = brute_force(nums, k, limit)
        if got != expected:
            print("Mismatch:", nums, k, limit, "got", got, "expected", expected)
            raise AssertionError

    # Provided examples.
    check([1, 2, 3], 2, 10, 6)
    check([0, 2, 3], -5, 12, -1)
    check([2, 2, 3, 3], 0, 9, 9)

    # Empty subsequence must not be accepted.
    check([1], 0, 10, -1)
    check([2], 0, 10, -1)
    check([0], 0, 10, 0)

    # All zeros.
    check([0, 0, 0], 0, 10, 0)
    check([0, 0, 0], 1, 10, -1)
    check([0] * 150, 0, 5000, 0)
    check([0] * 150, 1, 5000, -1)

    # Ones-only.
    check([1, 1], 0, 10, 1)
    check([1], 0, 10, -1)
    check([1, 1, 1], 0, 10, 1)
    check([1, 1, 1], 1, 10, 1)
    check([1, 1, 1], 2, 10, -1)
    check([1] * 150, 0, 5000, 1)
    check([1] * 150, 1, 5000, 1)
    check([1] * 150, -1, 5000, -1)

    # Negative k.
    check([1, 2, 3], -1, 10, 6)
    check([0, 2], -2, 10, 0)
    check([2, 0], 2, 10, 2)

    # Limit smaller than positive values.
    check([5, 5], 0, 4, -1)
    check([0, 5, 5], 0, 4, 0)
    check([5], 5, 4, -1)
    check([0, 5], -5, 4, 0)
    check([12, 0], 12, 1, 0)
    check([0, 12], -12, 1, 0)

    # k out of range.
    check([12], 13, 12, -1)
    check([12], -13, 12, -1)
    check([12], 12, 12, 12)
    check([12], 12, 11, -1)

    # Large repeated values with product cap.
    check([12] * 150, 0, 5000, 144)
    check([12] * 150, 12, 5000, 1728)
    check([12] * 150, -12, 5000, -1)

    # Random small cases against brute force.
    rng = random.Random(123456)
    for _ in range(200):
        n = rng.randint(1, 10)
        nums = [rng.randint(0, 12) for _ in range(n)]
        limit = rng.randint(1, 40)
        max_possible = 12 * n
        k = rng.randint(-max_possible, max_possible)
        check(nums, k, limit)

    # Random out-of-range k cases.
    for _ in range(50):
        n = rng.randint(1, 5)
        nums = [rng.randint(0, 12) for _ in range(n)]
        limit = rng.randint(1, 40)
        k = rng.choice([-1000, 1000])
        check(nums, k, limit, -1)

    print("All validation tests passed")


if __name__ == "__main__":
    run_validation()