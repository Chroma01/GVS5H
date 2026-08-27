from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        total = sum(nums)
        if k < -total or k > total:
            return -1

        width = 2 * total + 1
        offset = total
        mask = (1 << width) - 1
        target_bit = 1 << (k + offset)

        # Buckets 0..limit represent exact products.
        # The final bucket retains products > limit, because a later zero can
        # change such a product to zero.
        overflow = limit + 1
        even = [0] * (limit + 2)
        odd = [0] * (limit + 2)
        active = set()

        for x in nums:
            # Copies preserve skip transitions and prevent using x repeatedly.
            new_even = even.copy()
            new_odd = odd.copy()
            new_active = set(active)

            if x == 0:
                # Selecting zero flips selected-length parity while preserving sum.
                # Any old product, including overflow, becomes exact product zero.
                for p in active:
                    if even[p]:
                        new_odd[0] |= even[p]
                    if odd[p]:
                        new_even[0] |= odd[p]

                # Start singleton [0].
                new_odd[0] |= 1 << offset
                new_active.add(0)
            else:
                for p in active:
                    if p == overflow:
                        q = overflow
                    else:
                        product = p * x
                        q = product if product <= limit else overflow

                    # Next selected value is added after an even number selected,
                    # and subtracted after an odd number selected.
                    if even[p]:
                        new_odd[q] |= (even[p] << x) & mask
                    if odd[p]:
                        new_even[q] |= odd[p] >> x

                    new_active.add(q)

                # Start a singleton subsequence.
                q = x if x <= limit else overflow
                new_odd[q] |= 1 << (offset + x)
                new_active.add(q)

            even = new_even
            odd = new_odd
            active = new_active

        for product in range(limit, -1, -1):
            if (even[product] | odd[product]) & target_bit:
                return product

        return -1