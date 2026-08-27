```python
from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        max_sum = sum(nums)
        offset = max_sum
        size = max_sum * 2 + 1
        mask = (1 << size) - 1
        over = limit + 1  # sentinel index for product > limit
        # dp[parity][product_index] -> bitset of reachable alternating sums
        dp = [[0] * (limit + 2) for _ in range(2)]  # indices 0..limit, over = limit+1

        for a in nums:
            # snapshot before using current element
            old = [row[:] for row in dp]
            # start a new subsequence consisting only of a
            if a <= limit:
                dp[1][a] |= (1 << (offset + a))
            else:
                dp[1][over] |= (1 << (offset + a))
            # extend all existing non‑empty subsequences
            for parity in (0, 1):
                old_row = old[parity]
                new_parity = 1 - parity
                for prod_idx, bits in enumerate(old_row):
                    if bits == 0:
                        continue
                    # decide resulting product index
                    if prod_idx == over:
                        if a == 0:
                            new_prod_idx = 0
                        else:
                            new_prod_idx = over
                    else:
                        if a == 0:
                            new_prod_idx = 0
                        else:
                            new_prod = prod_idx * a
                            if new_prod > limit:
                                new_prod_idx = over
                            else:
                                new_prod_idx = new_prod
                    # shift the sum according to the sign of the new element
                    if parity == 0:
                        shifted = (bits << a) & mask
                    else:
                        shifted = bits >> a
                    dp[new_parity][new_prod_idx] |= shifted

        target = offset + k
        if not (0 <= target < size):
            return -1
        ans = -1
        for parity in (0, 1):
            row = dp[parity]
            for prod in range(limit + 1):
                if (row[prod] >> target) & 1:
                    if prod > ans:
                        ans = prod
        return ans
```