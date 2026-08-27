from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        bound = sum(nums)
        if k < -bound or k > bound:
            return -1

        offset = bound
        target_bit = 1 << (k + offset)
        mask = (1 << (2 * bound + 1)) - 1

        # Index limit + 1 represents any product greater than limit.
        # Such states matter because a later selected zero makes their
        # product become zero, which is within the limit.
        overflow = limit + 1
        even = [0] * (limit + 2)
        odd = [0] * (limit + 2)

        zero_sum_bit = 1 << offset

        for x in nums:
            next_even = even.copy()
            next_odd = odd.copy()

            if x == 0:
                reachable_even = 0
                reachable_odd = 0

                for p in range(limit + 2):
                    reachable_even |= even[p]
                    reachable_odd |= odd[p]

                # Appending zero flips length parity without changing sum.
                # Every previous product, including overflow, becomes zero.
                next_odd[0] |= reachable_even | zero_sum_bit
                next_even[0] |= reachable_odd
            else:
                # Products within the limit.
                for p in range(limit + 1):
                    if p == 0:
                        q = 0
                    else:
                        product = p * x
                        q = product if product <= limit else overflow

                    if even[p]:
                        next_odd[q] |= (even[p] << x) & mask
                    if odd[p]:
                        next_even[q] |= odd[p] >> x

                # An overflowing product remains overflowing after a
                # multiplication by any positive number.
                if even[overflow]:
                    next_odd[overflow] |= (even[overflow] << x) & mask
                if odd[overflow]:
                    next_even[overflow] |= odd[overflow] >> x

                # Singleton [x].
                singleton_product = x if x <= limit else overflow
                next_odd[singleton_product] |= 1 << (offset + x)

            even, odd = next_even, next_odd

        for product in range(limit, -1, -1):
            if (even[product] & target_bit) or (odd[product] & target_bit):
                return product

        return -1