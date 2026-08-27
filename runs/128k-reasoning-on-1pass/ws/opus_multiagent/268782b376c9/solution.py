from typing import List


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def check(T: int) -> bool:
            # T > 0 assumed
            cost = 0
            carry = 0
            for i in range(n - 1):
                p = points[i]
                need = -(-T // p) - carry
                if need <= 0:
                    cost += 1
                    carry = 0
                else:
                    cost += 2 * need - 1
                    carry = need - 1
                if cost > m:
                    return False
            # last index: no forward step needed if already covered by carry
            need = -(-T // points[n - 1]) - carry
            if need > 0:
                cost += 2 * need - 1
            return cost <= m

        lo = 0
        hi = (m // n + 1) * max(points)  # known infeasible
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if check(mid):
                lo = mid
            else:
                hi = mid
        return lo