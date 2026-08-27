from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        total = sum(nums)
        if abs(k) > total:
            return -1

        offset = total
        mask = (1 << (2 * offset + 1)) - 1
        target = 1 << (offset + k)
        zero_bit = 1 << offset

        # Zero-product reachability:
        # no_zero_even/odd: non-empty subsequences with no zero
        # zero_even/odd: subsequences containing at least one zero
        no_zero_even = 0
        no_zero_odd = 0
        zero_even = 0
        zero_odd = 0

        # Positive-product exact-product DP:
        # pos_even[p] / pos_odd[p] are bitsets of alternating sums
        # reachable with exact product p and even/odd length.
        pos_even = [0] * (limit + 1)
        pos_odd = [0] * (limit + 1)

        for x in nums:
            if x == 0:
                all_even = no_zero_even | zero_even
                all_odd = no_zero_odd | zero_odd

                # Taking this zero toggles parity but does not change sum.
                zero_even = zero_even | all_odd
                zero_odd = zero_odd | all_even | zero_bit
            else:
                nz_e = no_zero_even
                nz_o = no_zero_odd
                z_e = zero_even
                z_o = zero_odd

                single_bit = 1 << (offset + x)

                # Zero-free positive subsequences.
                no_zero_even = nz_e | (nz_o >> x)
                no_zero_odd = nz_o | ((nz_e << x) & mask) | single_bit

                # Zero-containing subsequences.
                zero_even = z_e | (z_o >> x)
                zero_odd = z_o | ((z_e << x) & mask)

                # Positive-product DP only uses positive numbers.
                if x <= limit:
                    old_even = pos_even
                    old_odd = pos_odd
                    new_even = old_even[:]
                    new_odd = old_odd[:]

                    # Single-element subsequence [x].
                    new_odd[x] |= single_bit

                    max_p = limit // x
                    for p in range(1, max_p + 1):
                        np = p * x

                        be = old_even[p]
                        if be:
                            new_odd[np] |= (be << x) & mask

                        bo = old_odd[p]
                        if bo:
                            new_even[np] |= bo >> x

                    pos_even = new_even
                    pos_odd = new_odd

        for p in range(limit, 0, -1):
            if (pos_even[p] & target) or (pos_odd[p] & target):
                return p

        if (zero_even & target) or (zero_odd & target):
            return 0

        return -1