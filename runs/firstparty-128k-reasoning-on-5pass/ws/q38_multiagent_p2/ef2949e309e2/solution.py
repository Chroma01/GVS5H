from typing import List

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        ans = 0

        def c2(x):
            return x * (x - 1) // 2 if x >= 2 else 0

        def comb(x, r):
            if r < 0 or r > x:
                return 0
            if r == 0:
                return 1
            if r == 1:
                return x
            if r == 2:
                return c2(x)
            return 0

        def distinct_pairs(freq, total):
            dp = c2(total)
            for cnt in freq.values():
                dp -= c2(cnt)
            return dp

        def cross_distinct(X, Y, totalX, totalY):
            if totalX == 0 or totalY < 2:
                return 0
            dp = distinct_pairs(Y, totalY)
            res = totalX * dp
            for v, xv in X.items():
                yv = Y.get(v, 0)
                if yv:
                    res -= xv * yv * (totalY - yv)
            return res % MOD

        for k in range(2, n - 2):
            m = nums[k]
            left = {}
            right = {}
            a = 0
            b = 0

            for i in range(k):
                v = nums[i]
                if v == m:
                    a += 1
                else:
                    left[v] = left.get(v, 0) + 1

            for i in range(k + 1, n):
                v = nums[i]
                if v == m:
                    b += 1
                else:
                    right[v] = right.get(v, 0) + 1

            A = k - a
            B = n - 1 - k - b

            auto = 0
            for x in range(3):
                for y in range(3):
                    if x + y >= 2:
                        auto += comb(a, x) * comb(A, 2 - x) * comb(b, y) * comb(B, 2 - y)

            exact = 0
            if a:
                exact += a * cross_distinct(left, right, A, B)
            if b:
                exact += b * cross_distinct(right, left, B, A)

            ans = (ans + auto + exact) % MOD

        return ans