from typing import List


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)

        # No-op answer: Kadane on the original array.
        M = nums[0]
        cur = nums[0]
        for i in range(1, n):
            a = nums[i]
            cur = a if cur < 0 else cur + a
            if cur > M:
                M = cur

        # If the best original subarray is non-positive, every element is <= 0;
        # deleting is never beneficial (also covers the non-empty pitfall).
        if M <= 0:
            return M

        # Prefix sums.
        P = [0] * (n + 1)
        for i in range(n):
            P[i + 1] = P[i] + nums[i]

        # E[i]: best subarray sum ending exactly at i.
        E = [0] * n
        E[0] = nums[0]
        for i in range(1, n):
            E[i] = nums[i] + (E[i - 1] if E[i - 1] > 0 else 0)

        # S[i]: best subarray sum starting exactly at i.
        S = [0] * n
        S[n - 1] = nums[n - 1]
        for i in range(n - 2, -1, -1):
            S[i] = nums[i] + (S[i + 1] if S[i + 1] > 0 else 0)

        # Only negative values can ever improve the answer.
        pos_by_val = {}
        for i, v in enumerate(nums):
            if v < 0:
                pos_by_val.setdefault(v, []).append(i)

        ans = M
        for x, pos in pos_by_val.items():
            pref_u = float("-inf")
            for b, p in enumerate(pos):
                L = E[p - 1] if p > 0 else 0
                if L < 0:
                    L = 0
                R = S[p + 1] if p + 1 < n else 0
                if R < 0:
                    R = 0
                u = L - P[p] + x * b
                if u > pref_u:
                    pref_u = u
                v = R + P[p + 1] - x * (b + 1)
                cand = pref_u + v
                if cand > ans:
                    ans = cand
        return ans