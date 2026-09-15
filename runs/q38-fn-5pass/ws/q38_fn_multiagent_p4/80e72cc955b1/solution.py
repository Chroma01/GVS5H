from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        max_r = 0
        for _, r in queries:
            if r > max_r:
                max_r = r

        powers = []
        p = 1
        while p <= max_r:
            powers.append(p)
            p *= 4

        def prefix_sum(n: int) -> int:
            """
            Returns sum_{x=1}^n f(x), where f(x) is the number of times
            x must be divided by 4 to become zero.

            f(x) equals the number of powers of 4 that are <= x.
            Therefore:
                sum_{x=1}^n f(x)
              = sum_{p in powers, p <= n} (n - p + 1)
            """
            if n <= 0:
                return 0

            total = 0
            for p in powers:
                if p > n:
                    break
                total += n - p + 1
            return total

        ans = 0
        for l, r in queries:
            total_work = prefix_sum(r) - prefix_sum(l - 1)
            ans += (total_work + 1) // 2

        return ans