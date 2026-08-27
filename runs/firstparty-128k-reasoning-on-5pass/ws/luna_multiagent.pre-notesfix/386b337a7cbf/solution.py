from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        offset = sum(nums)

        if k < -offset or k > offset:
            return -1

        # dp[product] = [bitset for even-length subsequences,
        #                 bitset for odd-length subsequences]
        dp = {}

        for value in nums:
            # Snapshot masks so states created during this iteration
            # cannot be reused by the same number.
            old_states = [
                (product, masks[0], masks[1])
                for product, masks in dp.items()
            ]

            # Every individual number forms a valid odd-length subsequence.
            singleton_product = value
            singleton_bit = 1 << (value + offset)
            if singleton_product <= limit:
                masks = dp.setdefault(singleton_product, [0, 0])
                masks[1] |= singleton_bit

            for product, even_mask, odd_mask in old_states:
                new_product = product * value
                if new_product > limit:
                    continue

                target = dp.setdefault(new_product, [0, 0])

                # Append value to an even-length subsequence:
                # its contribution is +value, and length becomes odd.
                target[1] |= even_mask << value

                # Append value to an odd-length subsequence:
                # its contribution is -value, and length becomes even.
                target[0] |= odd_mask >> value

        target_bit = 1 << (k + offset)
        for product in range(limit, -1, -1):
            masks = dp.get(product)
            if masks is not None and ((masks[0] | masks[1]) & target_bit):
                return product

        return -1