from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        M = sum(nums)
        # Any alternating sum s of a subsequence satisfies |s| <= M.
        if k < -M or k > M:
            return -1
        tbit = M + k  # bit index representing sum == k

        # ---------- Positive-product DP (elements 1..limit only) ----------
        # key = (used, parity, product) -> bitmask of achievable alternating sums
        # bit index i  <->  alternating sum (i - M)
        dp = {(0, 0, 1): 1 << M}  # empty subsequence: sum 0, product 1
        for x in nums:
            if x == 0 or x > limit:
                continue  # 0 -> product 0 (separate DP); x>limit -> product too big
            new_dp = dict(dp)
            # start a fresh subsequence with x (sign +, product x)
            bit = 1 << (M + x)
            key = (1, 1, x)
            prev = new_dp.get(key)
            new_dp[key] = bit if prev is None else prev | bit
            # extend every non-empty existing state
            for (used, parity, prod), mask in dp.items():
                if not used:
                    continue
                np = prod * x
                if np > limit:          # product is monotone for zero-free subsequences
                    continue
                nm = mask << x if parity == 0 else mask >> x
                key = (1, parity ^ 1, np)
                prev = new_dp.get(key)
                new_dp[key] = nm if prev is None else prev | nm
            dp = new_dp

        best = -1
        for (used, parity, prod), mask in dp.items():
            if used and ((mask >> tbit) & 1) and prod > best:
                best = prod
        if best >= 0:
            return best

        # ---------- Zero-containing feasibility DP (all elements) ----------
        # key = (parity, seen_zero) -> bitmask of achievable alternating sums
        z = {(0, False): 1 << M}
        for x in nums:
            new_z = dict(z)
            zx = (x == 0)
            for (parity, seen), mask in z.items():
                nm = mask << x if parity == 0 else mask >> x
                if nm == 0:
                    continue
                key = (parity ^ 1, seen or zx)
                prev = new_z.get(key)
                new_z[key] = nm if prev is None else prev | nm
            z = new_z

        for (parity, seen), mask in z.items():
            if seen and ((mask >> tbit) & 1):
                return 0
        return -1