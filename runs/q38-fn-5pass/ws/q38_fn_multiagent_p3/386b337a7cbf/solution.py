from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        total = sum(nums)
        if abs(k) > total:
            return -1

        offset = total
        target = k + offset

        # Positive-product DP: zero-free subsequences with product 1..limit.
        # dp0[prod] / dp1[prod] are bitsets of reachable alternating sums
        # for even / odd subsequence length.
        dp0 = [0] * (limit + 1)
        dp1 = [0] * (limit + 1)
        active = []  # (parity, product) states with nonzero bitset

        # all0/all1: all non-empty subsequences, regardless of product.
        # zero0/zero1: non-empty subsequences that contain at least one zero.
        all0 = 0
        all1 = 0
        zero0 = 0
        zero1 = 0

        for x in nums:
            old_all0 = all0
            old_all1 = all1
            old_zero0 = zero0
            old_zero1 = zero1

            if x == 0:
                # Append zero to all old subsequences: parity toggles, sum unchanged.
                if old_all0:
                    all1 |= old_all0
                if old_all1:
                    all0 |= old_all1

                singleton = 1 << offset  # sum 0, odd length
                all1 |= singleton

                # Appending zero makes product zero for every old subsequence.
                if old_all0:
                    zero1 |= old_all0
                if old_all1:
                    zero0 |= old_all1
                zero1 |= singleton

            else:
                # Update all-subsequence DP.
                if old_all0:
                    all1 |= old_all0 << x
                if old_all1:
                    all0 |= old_all1 >> x
                all1 |= 1 << (offset + x)

                # Update zero-product DP by appending positive x to old zero states.
                if old_zero0:
                    zero1 |= old_zero0 << x
                if old_zero1:
                    zero0 |= old_zero1 >> x

                # Update positive-product DP only when product can remain <= limit.
                if x <= limit:
                    if active:
                        snapshot = []
                        for p, prod in active:
                            bits = dp0[prod] if p == 0 else dp1[prod]
                            if bits:
                                snapshot.append((p, prod, bits))

                        for p, prod, bits in snapshot:
                            nprod = prod * x
                            if nprod > limit:
                                continue

                            if p == 0:
                                shifted = bits << x
                                if shifted:
                                    if dp1[nprod] == 0:
                                        active.append((1, nprod))
                                    dp1[nprod] |= shifted
                            else:
                                shifted = bits >> x
                                if shifted:
                                    if dp0[nprod] == 0:
                                        active.append((0, nprod))
                                    dp0[nprod] |= shifted

                    # Start a new positive-product subsequence with x.
                    bit = 1 << (offset + x)
                    if dp1[x] == 0:
                        active.append((1, x))
                    dp1[x] |= bit

        # Prefer positive products; zero is only used if no positive product works.
        for prod in range(limit, 0, -1):
            if dp0[prod] and ((dp0[prod] >> target) & 1):
                return prod
            if dp1[prod] and ((dp1[prod] >> target) & 1):
                return prod

        if ((zero0 >> target) & 1) or ((zero1 >> target) & 1):
            return 0

        return -1