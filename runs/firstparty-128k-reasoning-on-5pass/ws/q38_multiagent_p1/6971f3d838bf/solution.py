from typing import List

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        NEG = -10**30

        size = 1
        while size < n:
            size <<= 1

        sums = [0] * (2 * size)
        pref = [NEG] * (2 * size)
        suff = [NEG] * (2 * size)
        best = [NEG] * (2 * size)

        for i, v in enumerate(nums):
            pos = size + i
            sums[pos] = v
            pref[pos] = v
            suff[pos] = v
            best[pos] = v

        for i in range(size - 1, 0, -1):
            li = i << 1
            ri = li | 1

            ls = sums[li]
            rs = sums[ri]
            lp = pref[li]
            rp = pref[ri]
            lsu = suff[li]
            rsu = suff[ri]
            lb = best[li]
            rb = best[ri]

            sums[i] = ls + rs

            t = ls + rp
            pref[i] = lp if lp >= t else t

            t = rs + lsu
            suff[i] = rsu if rsu >= t else t

            b = lb if lb >= rb else rb
            t = lsu + rp
            if t > b:
                b = t
            best[i] = b

        ans = best[1]

        max1 = NEG
        max2 = NEG
        for v in nums:
            if v > max1:
                max2 = max1
                max1 = v
            elif v != max1 and v > max2:
                max2 = v

        groups = {}
        for i, v in enumerate(nums):
            if v < 0:
                if v in groups:
                    groups[v].append(i)
                else:
                    groups[v] = [i]

        def set_pos(p, val, sums=sums, pref=pref, suff=suff, best=best, size=size):
            i = size + p
            sums[i] = val
            pref[i] = val
            suff[i] = val
            best[i] = val
            i >>= 1

            while i:
                li = i << 1
                ri = li | 1

                ls = sums[li]
                rs = sums[ri]
                lp = pref[li]
                rp = pref[ri]
                lsu = suff[li]
                rsu = suff[ri]
                lb = best[li]
                rb = best[ri]

                sums[i] = ls + rs

                t = ls + rp
                pref[i] = lp if lp >= t else t

                t = rs + lsu
                suff[i] = rsu if rsu >= t else t

                b = lb if lb >= rb else rb
                t = lsu + rp
                if t > b:
                    b = t
                best[i] = b

                i >>= 1

        for x, idxs in groups.items():
            if len(idxs) >= n:
                continue

            for p in idxs:
                set_pos(p, 0)

            cand = best[1]
            if cand == 0:
                cand = max1 if max1 != x else max2

            if cand > ans:
                ans = cand

            for p in idxs:
                set_pos(p, x)

        return ans


if __name__ == "__main__":
    sol = Solution()

    assert sol.maxSubarraySum([-3, 2, -2, -1, 3, -2, 3]) == 7
    assert sol.maxSubarraySum([1, 2, 3, 4]) == 10

    assert sol.maxSubarraySum([-5]) == -5
    assert sol.maxSubarraySum([0]) == 0
    assert sol.maxSubarraySum([5]) == 5

    assert sol.maxSubarraySum([-5, -5]) == -5
    assert sol.maxSubarraySum([5, 5]) == 10

    assert sol.maxSubarraySum([-5, -2, -3]) == -2
    assert sol.maxSubarraySum([-1, -1, 1, -1, -1]) == 1
    assert sol.maxSubarraySum([-5, 1, -5, 1, -5]) == 2
    assert sol.maxSubarraySum([-2, 1, -1, 1, -2]) == 2

    assert sol.maxSubarraySum([0, -1, 0]) == 0
    assert sol.maxSubarraySum([-1, 0, -1, 0, -1]) == 0
    assert sol.maxSubarraySum([-1, -2, 0, -2, -1]) == 0

    assert sol.maxSubarraySum([-10, 5, -10, 5, -10]) == 10
    assert sol.maxSubarraySum([-1, 2, -1, 3, -1]) == 5

    import random
    random.seed(12345)

    def kadane(arr):
        cur = best = arr[0]
        for v in arr[1:]:
            cur = v if cur + v < v else cur + v
            best = cur if cur > best else best
        return best

    def brute(a):
        ans = kadane(a)
        for x in set(a):
            b = [v for v in a if v != x]
            if b:
                val = kadane(b)
                if val > ans:
                    ans = val
        return ans

    for _ in range(300):
        n = random.randint(1, 8)
        a = [random.randint(-5, 5) for _ in range(n)]
        assert sol.maxSubarraySum(a) == brute(a)