from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        total = sum(nums)
        if abs(k) > total:
            return -1

        L = limit
        if L < 0:
            return -1

        # Product categories:
        #   0          -> product is exactly 0 (subsequence contains a zero)
        #   1..L       -> positive product is exactly this value
        #   OVER = L+1 -> positive product is > L
        #
        # OVER is needed because a product that is currently too large can
        # later be multiplied by 0 and become a valid product 0.
        OVER = L + 1
        size = OVER + 1

        off = total
        mask = (1 << (2 * total + 1)) - 1
        target = 1 << (k + off)
        bit0 = 1 << off

        # dp0[p]: bitset of alternating sums for non-empty subsequences
        #         with product category p and even length.
        # dp1[p]: same, but odd length.
        dp0 = [0] * size
        dp1 = [0] * size

        # Exact positive products 1..L that currently have at least one state.
        active = []

        # OR of all even/odd bitsets over all product categories.
        # Used to append a zero in O(1) big-int operations.
        all0 = 0
        all1 = 0

        m = mask

        for x in nums:
            # Skip current number.
            new0 = dp0.copy()
            new1 = dp1.copy()

            if x == 0:
                # Append zero to any non-empty subsequence:
                # product becomes 0, parity flips, sum unchanged.
                new1[0] |= all0
                new0[0] |= all1

                # Start a new subsequence [0].
                new1[0] |= bit0
            else:
                # Start a new subsequence [x].
                if x <= L:
                    new1[x] |= 1 << (x + off)
                else:
                    new1[OVER] |= 1 << (x + off)

                # Append positive x to product-0 states: product stays 0.
                b = dp0[0]
                if b:
                    new1[0] |= (b << x) & m
                b = dp1[0]
                if b:
                    new0[0] |= b >> x

                # Append positive x to exact positive products.
                # If p*x exceeds limit, it becomes OVER.
                # All states that become OVER can be ORed first, then shifted once.
                high0 = dp0[OVER]
                high1 = dp1[OVER]
                maxp = L // x

                for p in active:
                    if p <= maxp:
                        q = p * x
                        b = dp0[p]
                        if b:
                            new1[q] |= (b << x) & m
                        b = dp1[p]
                        if b:
                            new0[q] |= b >> x
                    else:
                        b = dp0[p]
                        if b:
                            high0 |= b
                        b = dp1[p]
                        if b:
                            high1 |= b

                if high0:
                    new1[OVER] |= (high0 << x) & m
                if high1:
                    new0[OVER] |= high1 >> x

            dp0 = new0
            dp1 = new1

            # limit is the largest possible valid positive product.
            if (dp0[L] | dp1[L]) & target:
                return L

            # Recompute active exact products and global OR caches.
            active = []
            all0 = 0
            all1 = 0
            for p in range(size):
                a = dp0[p]
                b = dp1[p]
                all0 |= a
                all1 |= b
                if 0 < p < OVER and (a or b):
                    active.append(p)

        # Scan valid product categories from largest to smallest.
        for p in range(L, -1, -1):
            if (dp0[p] | dp1[p]) & target:
                return p

        return -1


if __name__ == "__main__":
    sol = Solution()
    samples = [
        ([1, 2, 3], 2, 10, 6),
        ([0, 2, 3], -5, 12, -1),
        ([2, 2, 3, 3], 0, 9, 9),
    ]

    for i, (nums, k, limit, expected) in enumerate(samples, 1):
        got = sol.maxProduct(nums, k, limit)
        print(f"Sample {i}: {'PASS' if got == expected else 'FAIL'} (got {got}, expected {expected})")