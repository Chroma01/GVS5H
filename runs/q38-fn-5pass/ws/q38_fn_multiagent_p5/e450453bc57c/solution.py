from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        if k == 0:
            return 0

        # Coordinate compression for Fenwick trees.
        vals = sorted(set(nums))
        m = len(vals)
        comp = {v: i + 1 for i, v in enumerate(vals)}
        idxs = [comp[v] for v in nums]

        # Fenwick trees: counts and sums of values in the current window.
        bit_cnt = [0] * (m + 1)
        bit_sum = [0] * (m + 1)

        def add(i: int, dc: int, ds: int) -> None:
            while i <= m:
                bit_cnt[i] += dc
                bit_sum[i] += ds
                i += i & -i

        def prefix_both(i: int):
            c = 0
            s = 0
            while i > 0:
                c += bit_cnt[i]
                s += bit_sum[i]
                i -= i & -i
            return c, s

        # Highest power of two <= m, for Fenwick order-statistic search.
        top = 1 << (m.bit_length() - 1)

        def kth(order: int) -> int:
            """Return compressed index of the order-th smallest element (1-indexed)."""
            idx = 0
            step = top
            while step:
                nxt = idx + step
                if nxt <= m and bit_cnt[nxt] < order:
                    idx = nxt
                    order -= bit_cnt[nxt]
                step >>= 1
            return idx + 1

        # Initialize first window.
        total = 0
        for i in range(x):
            idx = idxs[i]
            val = nums[i]
            add(idx, 1, val)
            total += val

        w = n - x + 1
        costs = [0] * w
        median_rank = (x + 1) // 2  # lower median

        for start in range(w):
            if start > 0:
                out_idx = idxs[start - 1]
                out_val = nums[start - 1]
                add(out_idx, -1, -out_val)
                total -= out_val

                in_idx = idxs[start + x - 1]
                in_val = nums[start + x - 1]
                add(in_idx, 1, in_val)
                total += in_val

            med_idx = kth(median_rank)
            med = vals[med_idx - 1]

            c_le, s_le = prefix_both(med_idx)

            # Cost using median med:
            # left part  (<= med): med * c_le - s_le
            # right part (> med):  (total - s_le) - med * (x - c_le)
            costs[start] = med * c_le - s_le + (total - s_le) - med * (x - c_le)

        # DP for choosing k non-overlapping windows.
        # dp_prev[i] = min cost to choose (t-1) windows in first i elements.
        INF = 10**30
        dp_prev = [0] * (n + 1)

        for t in range(1, k + 1):
            dp_cur = [INF] * (n + 1)
            prev = dp_prev
            cur = dp_cur
            cst = costs

            # Need at least t*x elements to place t windows of length x.
            for i in range(t * x, n + 1):
                best = cur[i - 1]
                cand = prev[i - x] + cst[i - x]
                if cand < best:
                    best = cand
                cur[i] = best

            dp_prev = dp_cur

        return dp_prev[n]