from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)

        # Coordinate-compress values so Fenwick trees can find medians.
        vals = sorted(set(nums))
        m = len(vals)
        comp = {v: i + 1 for i, v in enumerate(vals)}
        idxs = [comp[v] for v in nums]

        bit_count = [0] * (m + 1)
        bit_sum = [0] * (m + 1)

        def add(idx: int, dc: int, ds: int) -> None:
            while idx <= m:
                bit_count[idx] += dc
                bit_sum[idx] += ds
                idx += idx & -idx

        def prefix(idx: int):
            c = 0
            s = 0
            while idx:
                c += bit_count[idx]
                s += bit_sum[idx]
                idx -= idx & -idx
            return c, s

        top_bit = 1 << (m.bit_length() - 1)

        def kth(order: int) -> int:
            idx = 0
            step = top_bit
            while step:
                nxt = idx + step
                if nxt <= m and bit_count[nxt] < order:
                    idx = nxt
                    order -= bit_count[nxt]
                step >>= 1
            return idx + 1

        total_sum = 0
        for i in range(x):
            v = nums[i]
            add(idxs[i], 1, v)
            total_sum += v

        w = n - x + 1
        costs = [0] * w
        median_rank = (x + 1) // 2

        # Sliding-window median cost for every length-x window.
        for start in range(w):
            med_idx = kth(median_rank)
            med = vals[med_idx - 1]

            cnt_le, sum_le = prefix(med_idx)
            cnt_gt = x - cnt_le
            sum_gt = total_sum - sum_le

            costs[start] = (
                med * cnt_le - sum_le
                + sum_gt - med * cnt_gt
            )

            if start + x < n:
                out_v = nums[start]
                in_v = nums[start + x]

                add(idxs[start], -1, -out_v)
                total_sum -= out_v

                add(idxs[start + x], 1, in_v)
                total_sum += in_v

        if k == 1:
            return min(costs)

        INF = 10 ** 30
        dp = costs[:]

        # Weighted interval DP.
        # dp[i] = minimum cost for the current number of windows with last start i.
        for t in range(2, k + 1):
            # Convert dp into prefix minima: dp[i] = min(dp[0..i]).
            best = INF
            for i in range(w):
                if dp[i] < best:
                    best = dp[i]
                dp[i] = best

            new = [INF] * w
            first = (t - 1) * x

            for i in range(first, w):
                prev = dp[i - x]
                if prev < INF:
                    new[i] = costs[i] + prev

            dp = new

        return min(dp)