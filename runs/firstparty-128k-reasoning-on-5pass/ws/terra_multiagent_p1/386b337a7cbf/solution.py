from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        n = len(nums)
        max_sum = 12 * n

        if k < -max_sum or k > max_sum:
            return -1

        offset = max_sum
        width = 2 * max_sum + 1
        mask = (1 << width) - 1
        target_bit = 1 << (k + offset)

        # dp[parity][product] is a bitset of reachable alternating sums.
        # parity is chosen subsequence length modulo 2.
        dp = [[0] * (limit + 1) for _ in range(2)]

        for x in nums:
            # Snapshot states so this occurrence is appended at most once.
            old_even = dp[0][:]
            old_odd = dp[1][:]

            if x == 0:
                # Multiplying any existing product by zero yields product 0.
                # Alternating sum is unchanged and parity flips.
                even_sums = 0
                odd_sums = 0
                for bits in old_even:
                    even_sums |= bits
                for bits in old_odd:
                    odd_sums |= bits

                dp[1][0] |= even_sums
                dp[0][0] |= odd_sums

                # Singleton [0].
                dp[1][0] |= 1 << offset
                continue

            # Only source products p with p*x <= limit can be extended.
            for product in range(limit // x + 1):
                new_product = product * x

                bits = old_even[product]
                if bits:
                    # Appending at an even subsequence index adds x.
                    dp[1][new_product] |= (bits << x) & mask

                bits = old_odd[product]
                if bits:
                    # Appending at an odd subsequence index subtracts x.
                    dp[0][new_product] |= bits >> x

            # Start a new non-empty subsequence.
            if x <= limit:
                dp[1][x] |= 1 << (offset + x)

        for product in range(limit, -1, -1):
            if (dp[0][product] | dp[1][product]) & target_bit:
                return product

        return -1