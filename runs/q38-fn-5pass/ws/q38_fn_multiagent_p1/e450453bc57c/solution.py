from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        if k == 0 or x <= 1 or n == 0 or x > n or k * x > n:
            return 0

        vals = sorted(set(nums))
        m = len(vals)
        comp = {v: i + 1 for i, v in enumerate(vals)}
        idxs = [comp[v] for v in nums]
        del comp

        bit_count = [0] * (m + 1)
        bit_sum = [0] * (m + 1)

        def add(i: int, dc: int, ds: int, bc=bit_count, bs=bit_sum, mm=m) -> None:
            while i <= mm:
                bc[i] += dc
                bs[i] += ds
                i += i & -i

        def query(i: int, bc=bit_count, bs=bit_sum):
            c = 0
            s = 0
            while i > 0:
                c += bc[i]
                s += bs[i]
                i -= i & -i
            return c, s

        top = 1 << (m.bit_length() - 1)

        def kth(order: int, bc=bit_count, mm=m, start=top) -> int:
            idx = 0
            step = start
            while step:
                nxt = idx + step
                if nxt <= mm and bc[nxt] < order:
                    idx = nxt
                    order -= bc[nxt]
                step >>= 1
            return idx + 1

        total = 0
        for i in range(x):
            v = nums[i]
            add(idxs[i], 1, v)
            total += v

        rank = (x + 1) // 2
        window_count = n - x + 1
        costs = [0] * window_count

        def current_cost(
            total_sum: int,
            kth_func=kth,
            query_func=query,
            vals_list=vals,
            med_rank=rank,
            width=x,
        ) -> int:
            idx = kth_func(med_rank)
            med = vals_list[idx - 1]
            c, s = query_func(idx)
            return med * c - s + (total_sum - s) - med * (width - c)

        costs[0] = current_cost(total)

        for start in range(1, window_count):
            out_idx = idxs[start - 1]
            out_val = nums[start - 1]
            add(out_idx, -1, -out_val)
            total -= out_val

            in_idx = idxs[start + x - 1]
            in_val = nums[start + x - 1]
            add(in_idx, 1, in_val)
            total += in_val

            costs[start] = current_cost(total)

        if k == 1:
            return int(min(costs))

        INF = 10 ** 30
        dp_prev = [0] * (n + 1)

        for t in range(1, k + 1):
            dp_cur = [INF] * (n + 1)
            min_pos = t * x
            prev = dp_prev
            cur = dp_cur
            cst = costs
            xx = x

            for pos in range(min_pos, n + 1):
                best = cur[pos - 1]
                cand = prev[pos - xx] + cst[pos - xx]
                if cand < best:
                    best = cand
                cur[pos] = best

            dp_prev = dp_cur

        return int(dp_prev[n])