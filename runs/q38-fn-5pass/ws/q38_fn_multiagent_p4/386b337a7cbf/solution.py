from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        pos_sum = 0
        has_zero = False
        for x in nums:
            if x == 0:
                has_zero = True
            else:
                pos_sum += x

        # Zeros do not change the alternating sum, so the absolute sum
        # is bounded by the sum of positive elements.
        if abs(k) > pos_sum:
            return -1

        offset = pos_sum
        mask = (1 << (2 * offset + 1)) - 1
        target = 1 << (offset + k)

        # DP for positive-product subsequences only (no zero included).
        # dp_even[p]: bitset of alternating sums for non-empty subsequences
        #             with product p and even length.
        # dp_odd[p]: same, but odd length.
        dp_even = [0] * (limit + 1)
        dp_odd = [0] * (limit + 1)

        # Only iterate over products that are actually reachable.
        active = []
        in_active = [False] * (limit + 1)

        for x in nums:
            # A positive product cannot include 0, and cannot include x > limit.
            if x == 0 or x > limit:
                continue

            next_even = dp_even.copy()
            next_odd = dp_odd.copy()
            new_products = []

            # Start a new subsequence [x].
            if not in_active[x]:
                in_active[x] = True
                new_products.append(x)
            next_odd[x] |= 1 << (offset + x)

            if x == 1:
                # Product does not change; only parity and sum change.
                for p in active:
                    e = dp_even[p]
                    if e:
                        next_odd[p] |= (e << 1) & mask
                    o = dp_odd[p]
                    if o:
                        next_even[p] |= o >> 1
            else:
                for p in active:
                    np = p * x
                    if np > limit:
                        continue

                    if not in_active[np]:
                        in_active[np] = True
                        new_products.append(np)

                    e = dp_even[p]
                    if e:
                        next_odd[np] |= (e << x) & mask
                    o = dp_odd[p]
                    if o:
                        next_even[np] |= o >> 1

            active.extend(new_products)
            dp_even, dp_odd = next_even, next_odd

            # limit is the best possible positive product.
            if in_active[limit] and ((dp_even[limit] | dp_odd[limit]) & target):
                return limit

        # Best positive product, if any.
        for p in range(limit, 0, -1):
            if (dp_even[p] | dp_odd[p]) & target:
                return p

        # Fallback: product 0, which requires at least one zero.
        if not has_zero:
            return -1
        if k == 0:
            return 0

        # DP for existence of a zero-containing subsequence with sum k.
        # no_even/no_odd: positive-only subsequences (no zero yet).
        # has_even/has_odd: subsequences that already contain a zero.
        no_even = no_odd = has_even = has_odd = 0
        bit0 = 1 << offset

        for x in nums:
            ne_even, ne_odd = no_even, no_odd
            he_even, he_odd = has_even, has_odd

            if x == 0:
                # Start [0].
                he_odd |= bit0

                # Append zero to no-zero states.
                he_odd |= no_even
                he_even |= no_odd

                # Append zero to already-zero states.
                he_even |= has_odd
                he_odd |= has_even
            else:
                # Start positive-only [x].
                ne_odd |= 1 << (offset + x)

                # Append x to no-zero states.
                if no_even:
                    ne_odd |= (no_even << x) & mask
                if no_odd:
                    ne_even |= no_odd >> x

                # Append x to zero-containing states.
                if has_even:
                    he_odd |= (has_even << x) & mask
                if has_odd:
                    he_even |= has_odd >> x

            no_even, no_odd, has_even, has_odd = ne_even, ne_odd, he_even, he_odd

            if (has_even | has_odd) & target:
                return 0

        return -1