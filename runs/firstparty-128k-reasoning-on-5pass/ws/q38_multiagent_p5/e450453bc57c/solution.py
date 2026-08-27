from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)

        if x == n:
            arr = sorted(nums)
            med = arr[(n - 1) // 2]
            return sum(abs(v - med) for v in arr)

        if x == 2:
            costs = [abs(nums[i] - nums[i + 1]) for i in range(n - 1)]
        else:
            vals = sorted(set(nums))
            m = len(vals)
            if m == 1:
                return 0

            comp = {v: i + 1 for i, v in enumerate(vals)}
            idxs = [comp[v] for v in nums]

            bit_cnt = [0] * (m + 1)
            bit_sum = [0] * (m + 1)
            mm = m

            def add(idx: int, dc: int, ds: int, bc=bit_cnt, bs=bit_sum, mm=mm) -> None:
                while idx <= mm:
                    bc[idx] += dc
                    bs[idx] += ds
                    idx += idx & -idx

            def prefix(idx: int, bc=bit_cnt, bs=bit_sum):
                c = 0
                s = 0
                while idx:
                    c += bc[idx]
                    s += bs[idx]
                    idx -= idx & -idx
                return c, s

            top_bit = 1 << (m.bit_length() - 1)

            def kth(order: int, bc=bit_cnt, mm=mm, tb=top_bit) -> int:
                idx = 0
                bit = tb
                while bit:
                    nxt = idx + bit
                    if nxt <= mm and bc[nxt] < order:
                        idx = nxt
                        order -= bc[nxt]
                    bit >>= 1
                return idx + 1

            window_sum = 0
            for i in range(x):
                v = nums[i]
                window_sum += v
                add(idxs[i], 1, v)

            costs = [0] * (n - x + 1)
            rank = (x + 1) // 2
            last = n - x

            for s in range(last + 1):
                med_idx = kth(rank)
                med = vals[med_idx - 1]
                left_c, left_s = prefix(med_idx)
                costs[s] = med * left_c - left_s + (window_sum - left_s) - med * (x - left_c)

                if s == last:
                    break

                out_v = nums[s]
                in_v = nums[s + x]
                window_sum += in_v - out_v
                add(idxs[s], -1, -out_v)
                add(idxs[s + x], 1, in_v)

        if k == 1:
            return min(costs)

        INF = 10 ** 30
        prev = [0] * (n + 1)
        n1 = n + 1
        xx = x

        for t in range(1, k + 1):
            cur = [INF] * n1
            start = t * xx
            prev_l = prev
            cur_l = cur
            costs_l = costs

            for i in range(start, n1):
                best = cur_l[i - 1]
                take = prev_l[i - xx] + costs_l[i - xx]
                if take < best:
                    best = take
                cur_l[i] = best

            prev = cur

        return prev[n]