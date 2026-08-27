from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        total = sum(nums)
        if k > total or k < -total:
            return -1

        OFFSET = total
        WIDTH = 2 * total + 1
        CAP = limit + 1  # overflow token: any product > limit collapses here

        # dp[parity][sum + OFFSET] = set of capped products
        # parity 0: even-length subsequence (next picked element gets sign +)
        # parity 1: odd-length subsequence  (next picked element gets sign -)
        dp0 = [set() for _ in range(WIDTH)]
        dp1 = [set() for _ in range(WIDTH)]

        for x in nums:
            add0 = []  # (sum_index, product) additions to dp0 (even length)
            add1 = []  # additions to dp1 (odd length)

            # Start a new subsequence with x (index 0 -> sign +, odd length)
            add1.append((x + OFFSET, x if x <= limit else CAP))

            if x == 0:
                # Sum unchanged, parity flips, product resets to 0 (p * 0 = 0)
                for si in range(WIDTH):
                    if dp0[si]:
                        add1.append((si, 0))
                    if dp1[si]:
                        add0.append((si, 0))
            else:
                for si in range(WIDTH):
                    s = dp0[si]
                    if s:
                        ns = si + x  # even length -> x at even index -> +x
                        for p in s:
                            np = p * x
                            add1.append((ns, np if np <= limit else CAP))
                    s = dp1[si]
                    if s:
                        ns = si - x  # odd length -> x at odd index -> -x
                        for p in s:
                            np = p * x
                            add0.append((ns, np if np <= limit else CAP))

            for si, p in add0:
                dp0[si].add(p)
            for si, p in add1:
                dp1[si].add(p)

        ki = k + OFFSET
        best = -1
        for p in dp0[ki]:
            if p < CAP and p > best:
                best = p
        for p in dp1[ki]:
            if p < CAP and p > best:
                best = p
        return best