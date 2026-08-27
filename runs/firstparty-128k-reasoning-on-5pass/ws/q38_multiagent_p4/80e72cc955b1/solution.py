from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        ans = 0
        for l, r in queries:
            total = 0
            m = 0
            p = 1
            while p <= r:
                total += r - max(l, p) + 1
                m += 1
                p *= 4
            ans += max(m, (total + 1) // 2)
        return ans