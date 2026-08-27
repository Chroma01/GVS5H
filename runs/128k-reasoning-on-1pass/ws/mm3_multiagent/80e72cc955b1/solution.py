from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        """
        For a number x > 0 the number of times it must be selected to become 0 is
        f(x) = floor(log_4(x)) + 1.
        The total work for a query [l, r] is S = sum_{x=l}^{r} f(x).
        Each operation reduces the work of two numbers by exactly 1,
        therefore the minimum number of operations for the query is ceil(S/2)
        = (S + 1) // 2.
        The function f(x) is constant on intervals [4^{k-1}, 4^{k} - 1] (value k).
        There are at most 15 such intervals for x ≤ 10^9 because 4^15 > 10^9.
        We pre‑compute the powers of 4 and sum the contributions of each interval
        in O(log_4(max_val)) per query.
        """
        # pre‑compute powers of 4 up to > 1e9 (at most 16 values)
        pow4 = []
        p = 1
        while p <= 10**9:
            pow4.append(p)          # p = 4^i
            p <<= 2                  # multiply by 4 (same as p *= 4)
        # pow4[i] = 4**i for i = 0 .. len(pow4)-1

        def total_f(l: int, r: int) -> int:
            """Return Σ_{x=l}^{r} f(x) where f(x) = floor(log_4(x)) + 1 for x>0."""
            total = 0
            # iterate over intervals [4^{k-1}, 4^{k} - 1] (k starts at 1)
            for k in range(1, len(pow4) + 1):
                lo = pow4[k - 1]                 # 4^{k-1}
                hi = pow4[k] - 1 if k < len(pow4) else 10**9  # 4^{k} - 1, truncated at 1e9
                if lo > r:
                    break
                # count numbers of [l, r] that lie in this interval
                left = max(l, lo)
                right = min(r, hi)
                if left <= right:
                    total += k * (right - left + 1)
            return total

        answer = 0
        for l, r in queries:
            s = total_f(l, r)
            answer += (s + 1) // 2   # ceil(s / 2)
        return answer