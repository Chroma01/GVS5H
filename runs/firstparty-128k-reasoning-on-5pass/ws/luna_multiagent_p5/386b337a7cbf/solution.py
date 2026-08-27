from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        total = sum(nums)
        if k < -total or k > total:
            return -1

        offset = total
        width = 2 * total + 1

        # dp[parity][product] is a bitset of reachable alternating sums.
        # parity 0 means even subsequence length, parity 1 means odd length.
        dp = [[0] * (limit + 1) for _ in range(2)]

        for x in nums:
            old = dp
            dp = [old[0][:], old[1][:]]

            # Start a new non-empty subsequence containing only x.
            dp[1][x] |= 1 << (offset + x)

            # Append x to every subsequence from the previous snapshot.
            for product in range(limit + 1):
                even_sums = old[0][product]
                if even_sums:
                    new_product = product * x
                    if new_product <= limit:
                        # An element appended to an even-length subsequence
                        # receives a positive sign.
                        dp[1][new_product] |= even_sums << x

                odd_sums = old[1][product]
                if odd_sums:
                    new_product = product * x
                    if new_product <= limit:
                        # An element appended to an odd-length subsequence
                        # receives a negative sign.
                        dp[0][new_product] |= odd_sums >> x

        target_bit = 1 << (offset + k)
        for product in range(limit, -1, -1):
            if (dp[0][product] & target_bit) or (dp[1][product] & target_bit):
                return product

        return -1