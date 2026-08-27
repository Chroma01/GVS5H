from typing import List
from collections import defaultdict


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)

        # Prefix sums P[0..n], subarray nums[l..r] sums to P[r+1] - P[l].
        P = [0] * (n + 1)
        for i, v in enumerate(nums):
            P[i + 1] = P[i] + v

        # Segment tree over prefix indices [0..n].
        # Each node stores:
        #   mn   = minimum prefix value in its index range
        #   mx   = maximum prefix value in its index range
        #   best = max subarray sum fully inside the corresponding nums range
        #          = max(P[j] - P[i]) over i < j within the range
        size = 1
        while size < (n + 1):
            size <<= 1

        NEG = float('-inf')
        POS = float('inf')
        mn = [POS] * (2 * size)
        mx = [NEG] * (2 * size)
        best = [NEG] * (2 * size)

        for i in range(n + 1):
            mn[size + i] = P[i]
            mx[size + i] = P[i]
            # best stays -inf for a leaf (single prefix index => empty subarray)

        for i in range(size - 1, 0, -1):
            l, r = 2 * i, 2 * i + 1
            mn[i] = min(mn[l], mn[r])
            mx[i] = max(mx[l], mx[r])
            # cross term: take min prefix from left half, max prefix from right half
            best[i] = max(best[l], best[r], mx[r] - mn[l])

        def query(ql: int, qr: int) -> int:
            """Max subarray sum of nums[ql..qr] inclusive; -inf if ql > qr."""
            if ql > qr:
                return NEG
            # Query prefix indices [ql, qr + 1].
            lo, hi = ql + size, qr + 1 + size
            # Left-side accumulator (in query order) and right-side accumulator
            # (will be prepended), each as (mn, mx, best).
            lmn, lmx, lb = POS, NEG, NEG
            rmn, rmx, rb = POS, NEG, NEG
            has_l = has_r = False
            while lo <= hi:
                if lo % 2 == 1:
                    if has_l:
                        lb = max(lb, best[lo], mx[lo] - lmn)
                        lmn = min(lmn, mn[lo])
                        lmx = max(lmx, mx[lo])
                    else:
                        lmn, lmx, lb = mn[lo], mx[lo], best[lo]
                        has_l = True
                    lo += 1
                if hi % 2 == 0:
                    if has_r:
                        rb = max(best[hi], rb, rmx - mn[hi])
                        rmn = min(mn[hi], rmn)
                        rmx = max(mx[hi], rmx)
                    else:
                        rmn, rmx, rb = mn[hi], mx[hi], best[hi]
                        has_r = True
                    hi -= 1
                lo //= 2
                hi //= 2
            if not has_l:
                return rb
            if not has_r:
                return lb
            return max(lb, rb, rmx - lmn)

        # Case 1: perform no operation.
        ans = query(0, n - 1)

        # Group occurrence positions by value.
        positions = defaultdict(list)
        for i, v in enumerate(nums):
            positions[v].append(i)

        # Case 2: delete all occurrences of x (allowed only if array stays non-empty).
        for x, pos in positions.items():
            if len(pos) == n:
                continue  # deleting x would empty the array
            prev = -1
            for p in pos:
                # Segment nums[prev+1 .. p-1]
                cand = query(prev + 1, p - 1)
                if cand > ans:
                    ans = cand
                prev = p
            # Trailing segment nums[prev+1 .. n-1]
            cand = query(prev + 1, n - 1)
            if cand > ans:
                ans = cand

        return ans