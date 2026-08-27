from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        OFFSET = 1800
        SIZE = 3601
        FULL = (1 << SIZE) - 1

        # Max |alternating sum|: at most 75 positive picks of value <= 12
        if abs(k) > 900:
            return -1

        OVER = limit + 1  # sentinel: product exceeded the limit

        def cap(p, n):
            # new product after multiplying state product p by n
            if n == 0 or p == 0:
                return 0
            if p == OVER:
                return OVER
            v = p * n
            return v if v <= limit else OVER

        # dp[(parity, prod)] = bitmask of achievable alternating sums (bit s + OFFSET)
        dp = {}

        for num in nums:
            add = {}
            for (par, prod), mask in dp.items():
                if par == 0:
                    nm = (mask << num) & FULL
                else:
                    nm = mask >> num
                if nm == 0:
                    continue
                key = (1 - par, cap(prod, num))
                cur = add.get(key)
                add[key] = nm if cur is None else (cur | nm)

            # seed the singleton subsequence [num]
            key = (1, cap(1, num))
            bit = 1 << (num + OFFSET)
            cur = add.get(key)
            add[key] = bit if cur is None else (cur | bit)

            for key, m in add.items():
                cur = dp.get(key)
                dp[key] = m if cur is None else (cur | m)

        target = 1 << (k + OFFSET)
        best = -1
        for (par, prod), mask in dp.items():
            if prod != OVER and (mask & target):
                if prod > best:
                    best = prod
        return best