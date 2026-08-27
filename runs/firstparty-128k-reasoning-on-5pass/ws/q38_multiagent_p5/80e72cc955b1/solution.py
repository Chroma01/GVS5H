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

        def prefix(n: int) -> int:
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
            d = prefix(r) - prefix(l - 1)
            ans += (d + 1) // 2
        return ans