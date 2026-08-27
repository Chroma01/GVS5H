from typing import List


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        m = n - x + 1  # number of windows

        # Coordinate compression
        vals = sorted(set(nums))
        comp = {v: i + 1 for i, v in enumerate(vals)}  # 1-indexed
        size = len(vals)

        bit_cnt = [0] * (size + 1)
        bit_sum = [0] * (size + 1)

        def add(bit, i, delta):
            while i <= size:
                bit[i] += delta
                i += i & -i

        def prefix(bit, i):
            s = 0
            while i > 0:
                s += bit[i]
                i -= i & -i
            return s

        def kth(t):
            # smallest index i such that prefix count >= t (t >= 1)
            i = 0
            step = 1 << (size.bit_length() - 1)
            while step:
                ni = i + step
                if ni <= size and bit_cnt[ni] < t:
                    t -= bit_cnt[ni]
                    i = ni
                step >>= 1
            return i + 1

        cost = [0] * m

        # initialize first window
        for j in range(x):
            c = comp[nums[j]]
            add(bit_cnt, c, 1)
            add(bit_sum, c, nums[j])

        half = (x + 1) // 2  # lower median rank
        for i in range(m):
            if i > 0:
                out = comp[nums[i - 1]]
                add(bit_cnt, out, -1)
                add(bit_sum, out, -nums[i - 1])
                inn = comp[nums[i + x - 1]]
                add(bit_cnt, inn, 1)
                add(bit_sum, inn, nums[i + x - 1])

            med_idx = kth(half)
            med = vals[med_idx - 1]
            cnt_left = prefix(bit_cnt, med_idx)          # count of values <= med
            sum_left = prefix(bit_sum, med_idx)          # sum of values <= med
            total_sum = prefix(bit_sum, size)
            # cost = sum|a - med|
            cost[i] = med * cnt_left - sum_left + (total_sum - sum_left) - med * (x - cnt_left)

        # DP: exactly k non-overlapping windows (costs >= 0 so exactly k is optimal)
        INF = float('inf')
        prev = [0] * (m + 1)  # dp for j-1
        for j in range(1, k + 1):
            cur = [INF] * (m + 1)
            # window starting at index i (0-based) corresponds to cur position i+1
            # earliest start for j-th window is (j-1)*x
            start = (j - 1) * x
            best = INF
            # iterate i from start..m-1; cur[i+1] = min(cur[i], prev[i+1-x] + cost[i])
            for i in range(start, m):
                cand = prev[i + 1 - x] + cost[i]
                if cand < best:
                    best = cand
                cur[i + 1] = best
            prev = cur

        return prev[m]