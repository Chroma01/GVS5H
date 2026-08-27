from typing import List


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        m = n - x + 1  # number of windows (start indices 0..m-1)

        # ---- Step 1: sliding window cost to make all elements equal (to median) ----
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

        def kth(kth_val):
            # smallest index i such that prefix count >= kth_val (1-indexed)
            idx = 0
            step = 1 << (size.bit_length() - 1)
            while step:
                nxt = idx + step
                if nxt <= size and bit_cnt[nxt] < kth_val:
                    kth_val -= bit_cnt[nxt]
                    idx = nxt
                step >>= 1
            return idx + 1

        # initialize first window
        for v in nums[:x]:
            c = comp[v]
            add(bit_cnt, c, 1)
            add(bit_sum, c, v)

        cost = [0] * m
        half = (x + 1) // 2  # lower median rank

        for i in range(m):
            if i > 0:
                out_c = comp[nums[i - 1]]
                add(bit_cnt, out_c, -1)
                add(bit_sum, out_c, -nums[i - 1])
                in_c = comp[nums[i + x - 1]]
                add(bit_cnt, in_c, 1)
                add(bit_sum, in_c, nums[i + x - 1])

            med_idx = kth(half)
            med = vals[med_idx - 1]
            cnt_left = prefix(bit_cnt, med_idx)   # count of elements <= med
            sum_left = prefix(bit_sum, med_idx)   # sum of elements <= med
            total_sum = prefix(bit_sum, size)
            cost[i] = med * cnt_left - sum_left + (total_sum - sum_left) - med * (x - cnt_left)

        # ---- Step 2: DP to pick k non-overlapping windows with min total cost ----
        INF = float('inf')
        # prev[i] = min cost choosing j-1 windows among starts 0..i
        # cur[i]  = min(cur[i-1], prev[i-x] + cost[i])
        prev = [0] * m  # j = 0 row: zero cost
        for j in range(1, k + 1):
            cur = [INF] * m
            start = (j - 1) * x  # earliest feasible start for the j-th window
            for i in range(start, m):
                best = cur[i - 1] if i > 0 else INF
                if j == 1:
                    take = cost[i]
                else:
                    take = prev[i - x] + cost[i] if i - x >= 0 else INF
                if take < best:
                    best = take
                cur[i] = best
            prev = cur

        return prev[m - 1]