from typing import List
from collections import defaultdict

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        # Prefix sums P[0..n]
        P = [0] * (n + 1)
        for i, v in enumerate(nums):
            P[i + 1] = P[i] + v

        # Sparse tables for range min and range max over P
        st_min = [P[:]]
        st_max = [P[:]]
        j = 1
        while (1 << j) <= n + 1:
            prev_min = st_min[-1]
            prev_max = st_max[-1]
            length = (n + 1) - (1 << j) + 1
            half = 1 << (j - 1)
            cur_min = [0] * length
            cur_max = [0] * length
            for i in range(length):
                a = prev_min[i]
                b = prev_min[i + half]
                cur_min[i] = a if a < b else b
                a = prev_max[i]
                b = prev_max[i + half]
                cur_max[i] = a if a > b else b
            st_min.append(cur_min)
            st_max.append(cur_max)
            j += 1

        log_table = [0] * (n + 2)
        for i in range(2, n + 2):
            log_table[i] = log_table[i >> 1] + 1

        def range_min(l: int, r: int) -> int:  # inclusive
            k = log_table[r - l + 1]
            a = st_min[k][l]
            b = st_min[k][r - (1 << k) + 1]
            return a if a < b else b

        def range_max(l: int, r: int) -> int:  # inclusive
            k = log_table[r - l + 1]
            a = st_max[k][l]
            b = st_max[k][r - (1 << k) + 1]
            return a if a > b else b

        def gap_stats(l: int, r: int):
            # For gap nums[l..r] (inclusive, non-empty):
            # S  = total sum
            # MP = max prefix sum
            # MS = max suffix sum
            # MM = max subarray sum
            S = P[r + 1] - P[l]
            hi = range_max(l + 1, r + 1)
            lo = range_min(l, r)
            MP = hi - P[l]
            MS = P[r + 1] - lo
            MM = hi - lo
            return S, MP, MS, MM

        # No-operation answer: max subarray sum of the whole array
        ans = gap_stats(0, n - 1)[3]

        # Group positions by value
        positions = defaultdict(list)
        for i, v in enumerate(nums):
            positions[v].append(i)

        NEG_INF = float('-inf')

        for v, pos in positions.items():
            if len(pos) == n:
                # Deleting v empties the array — not allowed
                continue
            # Kadane-like scan over the gaps (segments between occurrences of v).
            # After deletion the gaps concatenate, so subarrays may span gaps.
            best = NEG_INF        # best subarray sum seen so far for this deletion
            best_suffix = NEG_INF # best sum of a subarray ending at the current gap's end
            prev = -1
            gaps = []
            for p in pos:
                if p - 1 >= prev + 1:
                    gaps.append((prev + 1, p - 1))
                prev = p
            if prev + 1 <= n - 1:
                gaps.append((prev + 1, n - 1))

            for l, r in gaps:
                S, MP, MS, MM = gap_stats(l, r)
                # Candidate: subarray entirely inside this gap, or one that
                # extends a previous suffix with a prefix of this gap.
                cand = MM
                if best_suffix != NEG_INF:
                    ext = best_suffix + MP
                    if ext > cand:
                        cand = ext
                if cand > best:
                    best = cand
                # Update best suffix ending at end of this gap
                new_suffix = MS
                if best_suffix != NEG_INF:
                    ext = best_suffix + S
                    if ext > new_suffix:
                        new_suffix = ext
                best_suffix = new_suffix

            if best > ans:
                ans = best

        return ans