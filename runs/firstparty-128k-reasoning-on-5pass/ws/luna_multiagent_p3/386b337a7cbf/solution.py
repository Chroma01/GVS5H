from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        # dp[parity][alternating_sum] = maximum reachable product
        # parity is the selected subsequence length modulo 2.
        dp = [{}, {}]

        for x in nums:
            old_even = dp[0].copy()
            old_odd = dp[1].copy()

            # Start a new subsequence containing only x.
            if x <= limit:
                if x > dp[1].get(x, -1):
                    dp[1][x] = x

            # Append x to every subsequence formed before this element.
            for parity, states in enumerate((old_even, old_odd)):
                next_parity = 1 - parity
                contribution_sign = 1 if parity == 0 else -1

                for alternating_sum, product in states.items():
                    new_sum = alternating_sum + contribution_sign * x
                    new_product = product * x

                    # Product zero must be retained; positive products above
                    # the limit cannot be used in any valid continuation.
                    if new_product <= limit:
                        if new_product > dp[next_parity].get(new_sum, -1):
                            dp[next_parity][new_sum] = new_product

        answer = max(dp[0].get(k, -1), dp[1].get(k, -1))
        return answer