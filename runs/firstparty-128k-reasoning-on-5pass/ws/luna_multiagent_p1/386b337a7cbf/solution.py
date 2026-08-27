from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        n = len(nums)
        offset = 12 * n

        if k < -offset or k > offset:
            return -1

        target_bit = 1 << (offset + k)

        # Reachable alternating sums for non-empty subsequences,
        # separated by subsequence-length parity.
        all_even = 0
        all_odd = 0

        # Reachable sums for non-empty subsequences containing zero.
        zero_even = 0
        zero_odd = 0

        for x in nums:
            new_all_even = all_even
            new_all_odd = all_odd
            new_zero_even = zero_even
            new_zero_odd = zero_odd

            # Singleton [x].
            new_all_odd |= 1 << (offset + x)

            # Append x to an existing subsequence.
            # Appending to even length adds x; appending to odd length subtracts x.
            new_all_odd |= all_even << x
            new_all_even |= all_odd >> x

            # Append x to a subsequence already containing zero.
            new_zero_odd |= zero_even << x
            new_zero_even |= zero_odd >> x

            if x == 0:
                # Singleton [0].
                new_zero_odd |= 1 << offset

                # Appending zero to any existing subsequence creates
                # a zero-containing subsequence without changing its sum.
                new_zero_odd |= all_even
                new_zero_even |= all_odd

            all_even, all_odd = new_all_even, new_all_odd
            zero_even, zero_odd = new_zero_even, new_zero_odd

        has_zero_solution = bool(
            (zero_even & target_bit) or (zero_odd & target_bit)
        )

        # For positive products, each product stores masks of reachable
        # alternating sums for even- and odd-length subsequences.
        dp_even = [0] * (limit + 1)
        dp_odd = [0] * (limit + 1)

        active = []
        present = [False] * (limit + 1)

        for x in nums:
            if x == 0:
                continue

            new_even = dp_even[:]
            new_odd = dp_odd[:]

            # Only products active before this element may be extended.
            old_count = len(active)

            # Singleton [x].
            if x <= limit:
                if not present[x]:
                    present[x] = True
                    active.append(x)
                new_odd[x] |= 1 << (offset + x)

            # Extend subsequences formed from earlier elements.
            for index in range(old_count):
                product = active[index]
                new_product = product * x

                if new_product > limit:
                    continue

                if not present[new_product]:
                    present[new_product] = True
                    active.append(new_product)

                even_sums = dp_even[product]
                odd_sums = dp_odd[product]

                if even_sums:
                    new_odd[new_product] |= even_sums << x
                if odd_sums:
                    new_even[new_product] |= odd_sums >> x

            dp_even, dp_odd = new_even, new_odd

        for product in range(limit, 0, -1):
            if (dp_even[product] & target_bit) or (
                dp_odd[product] & target_bit
            ):
                return product

        return 0 if has_zero_solution else -1