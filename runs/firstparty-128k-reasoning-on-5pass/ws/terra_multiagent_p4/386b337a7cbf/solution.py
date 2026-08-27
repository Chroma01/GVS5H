from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        total = sum(nums)
        if k < -total or k > total:
            return -1

        offset = total
        width = 2 * total + 1
        mask = (1 << width) - 1
        target_bit = 1 << (k + offset)

        # Alternating-sum reachability for all non-empty subsequences.
        # The zero variants represent subsequences containing at least one zero.
        all_even = all_odd = 0
        zero_even = zero_odd = 0

        # dp[product] = [even_length_sums, odd_length_sums].
        # These states contain only non-empty subsequences made entirely
        # of positive values, with product at most limit.
        dp = {}

        for x in nums:
            old_all_even, old_all_odd = all_even, all_odd
            old_zero_even, old_zero_odd = zero_even, zero_odd

            # Update zero-product subsequence reachability.
            if x == 0:
                # A zero can be selected alone or appended to any old subsequence.
                zero_odd |= 1 << offset
                zero_odd |= old_all_even
                zero_even |= old_all_odd
            else:
                # Append this positive element to an already zero-containing state.
                zero_odd |= (old_zero_even << x) & mask
                zero_even |= old_zero_odd >> x

            # Update reachability for every non-empty subsequence.
            all_odd |= (old_all_even << x) & mask
            all_even |= old_all_odd >> x
            all_odd |= 1 << (offset + x)

            # Positive-product DP does not include zeros. Values larger than
            # limit cannot belong to a valid positive-product subsequence.
            if x == 0 or x > limit:
                continue

            if x == 1:
                # Product remains unchanged, so snapshot sources to prevent
                # selecting this same element multiple times.
                sources = [(p, states[0], states[1]) for p, states in dp.items()]
                for p, even_bits, odd_bits in sources:
                    states = dp[p]
                    states[1] |= (even_bits << 1) & mask
                    states[0] |= odd_bits >> 1
            else:
                # Descending order prevents a newly generated product from
                # becoming a source during this element's iteration.
                for p in sorted(dp.keys(), reverse=True):
                    new_product = p * x
                    if new_product > limit:
                        continue

                    even_bits, odd_bits = dp[p]
                    if new_product not in dp:
                        dp[new_product] = [0, 0]

                    states = dp[new_product]
                    states[1] |= (even_bits << x) & mask
                    states[0] |= odd_bits >> x

            # Start a new positive subsequence using x alone.
            if x not in dp:
                dp[x] = [0, 0]
            dp[x][1] |= 1 << (offset + x)

        # Positive products are preferred over zero, and searched descending.
        for product in range(limit, 0, -1):
            states = dp.get(product)
            if states is not None and ((states[0] | states[1]) & target_bit):
                return product

        if (zero_even | zero_odd) & target_bit:
            return 0

        return -1