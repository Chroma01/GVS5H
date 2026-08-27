from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        total = sum(nums)
        if k < -total or k > total:
            return -1

        # State: (alternating_sum, length_parity) -> attainable products.
        # parity 0 means even length, parity 1 means odd length.
        dp = {}

        for x in nums:
            additions = {}

            # Add the one-element subsequence [x].
            key = (x, 1)
            additions.setdefault(key, set()).add(x)

            # Extend every subsequence formed before this element.
            for (alt_sum, parity), products in dp.items():
                new_sum = alt_sum + x if parity == 0 else alt_sum - x
                new_parity = parity ^ 1
                target = additions.setdefault((new_sum, new_parity), set())

                if x == 0:
                    # Every existing product becomes zero, including zero products.
                    target.add(0)
                else:
                    for product in products:
                        new_product = product * x
                        if new_product <= limit:
                            target.add(new_product)

            # Merge only after all transitions are generated, preventing reuse
            # of the current element within the same iteration.
            for key, products in additions.items():
                dp.setdefault(key, set()).update(products)

        answer = -1
        for parity in (0, 1):
            products = dp.get((k, parity))
            if products:
                answer = max(answer, max(products))

        return answer