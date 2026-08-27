from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        vals = sorted(set(nums))
        m = len(vals)
        comp = {v: i + 1 for i, v in enumerate(vals)}
        idx = [comp[v] for v in nums]
        del comp

        bitc = [0] * (m + 1)
        bits = [0] * (m + 1)
        freq = [0] * (m + 1)

        def add(i, dc, ds, bitc=bitc, bits=bits, freq=freq, m=m):
            freq[i] += dc
            while i <= m:
                bitc[i] += dc
                bits[i] += ds
                i += i & -i

        def pref2(i, bitc=bitc, bits=bits):
            cnt = 0
            s = 0
            while i:
                cnt += bitc[i]
                s += bits[i]
                i -= i & -i
            return cnt, s

        top_bit = 1 << (m.bit_length() - 1)

        def kth(r, bitc=bitc, m=m, top_bit=top_bit):
            pos = 0
            step = top_bit
            while step:
                nxt = pos + step
                if nxt <= m and bitc[nxt] < r:
                    pos = nxt
                    r -= bitc[nxt]
                step >>= 1
            return pos + 1

        total = 0
        for i in range(x):
            v = nums[i]
            add(idx[i], 1, v)
            total += v

        rank = (x + 1) // 2
        limit = n - x + 1
        costs = [0] * limit

        def calc_cost(total, vals=vals, freq=freq, x=x, rank=rank, kth=kth, pref2=pref2):
            mi = kth(rank)
            med = vals[mi - 1]
            cnt_less, sum_less = pref2(mi - 1)
            cnt_eq = freq[mi]
            cnt_le = cnt_less + cnt_eq
            sum_le = sum_less + med * cnt_eq
            return med * cnt_less - sum_less + (total - sum_le) - med * (x - cnt_le)

        costs[0] = calc_cost(total)
        for i in range(x, n):
            out = nums[i - x]
            add(idx[i - x], -1, -out)
            total -= out
            inn = nums[i]
            add(idx[i], 1, inn)
            total += inn
            costs[i - x + 1] = calc_cost(total)

        INF = 10 ** 18
        prev = [0] * (n + 1)
        for t in range(1, k + 1):
            curr = [INF] * (n + 1)
            p = prev
            c = curr
            cst = costs
            for j in range((t - 1) * x, limit):
                i = j + x
                take = p[j] + cst[j]
                best = c[i - 1]
                if take < best:
                    best = take
                c[i] = best
            prev = curr
        return prev[n]