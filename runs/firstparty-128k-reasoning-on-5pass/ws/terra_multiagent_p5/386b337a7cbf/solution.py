from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        n = len(nums)
        bound = 12 * ((n + 1) // 2)

        if k < -bound or k > bound:
            return -1

        width = 2 * bound + 1
        offset = bound
        mask = (1 << width) - 1

        # even[p] / odd[p] store bitsets of alternating sums for non-empty
        # positive-product subsequences of even / odd chosen length.
        even = [0] * (limit + 1)
        odd = [0] * (limit + 1)

        # Union over every currently reachable positive product state.
        # This permits converting all positive states to product zero in O(1)
        # bitset operations when the current element is zero.
        positive_even_union = 0
        positive_odd_union = 0

        # Product-zero non-empty subsequences, separated by selected-length parity.
        zero_even = 0
        zero_odd = 0

        for x in nums:
            old_zero_even = zero_even
            old_zero_odd = zero_odd

            if x == 0:
                # Append zero to previous zero-product subsequences.
                # Its alternating contribution is zero, so only parity changes.
                zero_odd |= old_zero_even
                zero_even |= old_zero_odd

                # Append zero to any positive-product subsequence.
                zero_odd |= positive_even_union
                zero_even |= positive_odd_union

                # Start singleton [0].
                zero_odd |= 1 << offset
                continue

            # Append a positive x to prior zero-product subsequences.
            # Product stays zero, while alternating sum changes according to parity.
            zero_odd |= (old_zero_even << x) & mask
            zero_even |= old_zero_odd >> x

            # Append x to positive-product subsequences.
            # Descending traversal prevents reuse of this occurrence for x > 1.
            max_source_product = limit // x
            for product in range(max_source_product, 0, -1):
                source_even = even[product]
                source_odd = odd[product]

                if source_even == 0 and source_odd == 0:
                    continue

                new_product = product * x

                # Appending after even length gives a positive contribution.
                if source_even:
                    added = (source_even << x) & mask
                    odd[new_product] |= added
                    positive_odd_union |= added

                # Appending after odd length gives a negative contribution.
                if source_odd:
                    added = source_odd >> x
                    even[new_product] |= added
                    positive_even_union |= added

            # Add singleton only after transitions. This is necessary for x == 1,
            # where source and destination product indices are identical.
            if x <= limit:
                singleton = 1 << (offset + x)
                odd[x] |= singleton
                positive_odd_union |= singleton

        target_bit = 1 << (offset + k)

        for product in range(limit, 0, -1):
            if (even[product] | odd[product]) & target_bit:
                return product

        if (zero_even | zero_odd) & target_bit:
            return 0

        return -1