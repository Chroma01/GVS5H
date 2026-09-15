from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)

        # Coordinate-compress values for Fenwick trees.
        vals = sorted(set(nums))
        size = len(vals)
        comp_map = {v: i + 1 for i, v in enumerate(vals)}
        comp = [comp_map[v] for v in nums]

        # Fenwick trees: counts and sums of active window values.
        bit_cnt = [0] * (size + 1)
        bit_sum = [0] * (size + 1)

        def add(i, dc, ds, bc=bit_cnt, bs=bit_sum, sz=size):
            while i <= sz:
                bc[i] += dc
                bs[i] += ds
                i += i & -i

        total = 0
        for i in range(x):
            v = nums[i]
            total += v
            add(comp[i], 1, v)

        # Lower median rank.
        rank = (x + 1) // 2
        bitmask = 1 << (size.bit_length() - 1)

        def get_cost(total_sum, bc=bit_cnt, bs=bit_sum, vals=vals, sz=size,
                     bitmask=bitmask, rank=rank, x=x):
            # Find largest Fenwick prefix with count < rank.
            # This gives all values strictly smaller than the lower median.
            idx = 0
            cnt_less = 0
            sum_less = 0
            step = bitmask
            r = rank

            while step:
                nxt = idx + step
                if nxt <= sz and cnt_less + bc[nxt] < r:
                    cnt_less += bc[nxt]
                    sum_less += bs[nxt]
                    idx = nxt
                step >>= 1

            med = vals[idx]

            # Cost to make all elements equal to med:
            # sum_{v < med} (med - v) + sum_{v > med} (v - med).
            # Elements equal to med contribute 0 and cancel algebraically:
            # total - med*x + 2 * (med*cnt_less - sum_less)
            return total_sum - med * x + 2 * (med * cnt_less - sum_less)

        m = n - x + 1
        costs = [0] * m
        costs[0] = get_cost(total)

        add_local = add
        get_cost_local = get_cost
        nums_local = nums
        comp_local = comp

        # Slide the window and compute every window cost.
        for start in range(1, m):
            out_idx = start - 1
            in_idx = start + x - 1

            out_v = nums_local[out_idx]
            in_v = nums_local[in_idx]

            total += in_v - out_v
            add_local(comp_local[out_idx], -1, -out_v)
            add_local(comp_local[in_idx], 1, in_v)

            costs[start] = get_cost_local(total)

        if k == 1:
            return min(costs)

        # DP over selected window starts.
        # dp[i] = minimum cost for current number of windows with last start i.
        INF = 10 ** 30
        dp = costs[:]

        for t in range(2, k + 1):
            new = [INF] * m
            best = INF
            min_start = (t - 1) * x

            dp_local = dp
            costs_local = costs
            x_local = x

            for i in range(m):
                if i >= x_local:
                    v = dp_local[i - x_local]
                    if v < best:
                        best = v

                if i >= min_start and best < INF:
                    new[i] = best + costs_local[i]

            dp = new

        return min(dp)