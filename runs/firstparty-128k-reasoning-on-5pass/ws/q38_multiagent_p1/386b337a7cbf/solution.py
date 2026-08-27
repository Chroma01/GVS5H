from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        offset = sum(nums)
        if abs(k) > offset:
            return -1

        mask = (1 << (2 * offset + 1)) - 1
        bit0 = 1 << offset
        target = 1 << (k + offset)

        # dp0[p] / dp1[p]: bitsets of alternating sums for non-empty subsequences
        # with exact positive product p, even / odd length, and no zero.
        dp0 = [0] * (limit + 1)
        dp1 = [0] * (limit + 1)

        # zero0 / zero1: bitsets for non-empty subsequences with product 0.
        zero0 = 0
        zero1 = 0

        # all0 / all1: capless reachability for all non-empty subsequences.
        all0 = 0
        all1 = 0

        for x in nums:
            if x == 0:
                old_zero0, old_zero1 = zero0, zero1
                old_all0, old_all1 = all0, all1

                # Taking zero keeps the sum unchanged and flips parity.
                zero0 = old_zero0 | old_all1
                zero1 = old_zero1 | old_all0 | bit0

                all0 = old_all0 | old_all1
                all1 = old_all1 | old_all0 | bit0

            else:
                old_dp0 = dp0[:]
                old_dp1 = dp1[:]
                old_zero0, old_zero1 = zero0, zero1
                old_all0, old_all1 = all0, all1

                # Positive-product transitions.
                max_q = limit // x
                for q in range(1, max_q + 1):
                    idx = q * x

                    b0 = old_dp0[q]
                    if b0:
                        # Even length: next element is added.
                        dp1[idx] |= (b0 << x) & mask

                    b1 = old_dp1[q]
                    if b1:
                        # Odd length: next element is subtracted.
                        dp0[idx] |= (b1 >> x) & mask

                # Singleton subsequence [x].
                if x <= limit:
                    dp1[x] |= (bit0 << x) & mask

                # Zero-product transitions: only previous zero-product states
                # remain zero-product after multiplying by a positive x.
                zero0 = old_zero0 | ((old_zero1 >> x) & mask)
                zero1 = old_zero1 | ((old_zero0 << x) & mask)

                # Capless all-subsequence reachability.
                all0 = old_all0 | ((old_all1 >> x) & mask)
                all1 = old_all1 | ((old_all0 << x) & mask) | ((bit0 << x) & mask)

        # Prefer the largest positive product within the limit.
        for p in range(limit, 0, -1):
            if (dp0[p] | dp1[p]) & target:
                return p

        # Otherwise, product 0 is the best possible if reachable.
        if (zero0 | zero1) & target:
            return 0

        return -1


if __name__ == "__main__":
    sol = Solution()
    assert sol.maxProduct([1, 2, 3], 2, 10) == 6
    assert sol.maxProduct([0, 2, 3], -5, 12) == -1
    assert sol.maxProduct([2, 2, 3, 3], 0, 9) == 9