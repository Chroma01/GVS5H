from typing import List


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)

        # ---------- (a) sliding-window median-deviation costs ----------
        vals = sorted(set(nums))
        m = len(vals)
        comp_of = {v: i + 1 for i, v in enumerate(vals)}   # 1-based BIT index
        comp = [comp_of[v] for v in nums]

        lo = vals[0]
        OFF = -lo if lo < 0 else 0                # make every value non-negative
        hi = vals[-1] + OFF
        SH = (hi * n).bit_length() + 1            # bits reserved for the sum part
        ONE = 1 << SH                             # a "count" unit
        MASK = ONE - 1
        # packed Fenwick: node = count * 2^SH + sum(shifted values)
        deltas = [ONE + (v + OFF) for v in nums]
        tree = [0] * (m + 1)

        HP = 1
        while HP * 2 <= m:
            HP *= 2

        r = (x + 1) // 2          # rank (1-based) of the lower median
        total = 0
        cost = [0] * (n - x + 1)

        for i in range(n):
            total += nums[i]
            d = deltas[i]
            j = comp[i]
            while j <= m:
                tree[j] += d
                j += j & (-j)
            if i >= x:
                total -= nums[i - x]
                d = deltas[i - x]
                j = comp[i - x]
                while j <= m:
                    tree[j] -= d
                    j += j & (-j)
            if i >= x - 1:
                # binary-lifting descent for the r-th smallest of the window
                pos = 0
                rem = r
                acc = 0
                pw = HP
                while pw:
                    np_ = pos + pw
                    if np_ <= m:
                        t = tree[np_]
                        c = t >> SH
                        if c < rem:
                            pos = np_
                            rem -= c
                            acc += t
                    pw >>= 1
                med = vals[pos]                 # median value
                cl = r - rem                    # count of elements strictly < med
                sl = (acc & MASK) - cl * OFF    # their real sum
                cost[i - x + 1] = (med * cl - sl) + (total - sl) - med * (x - cl)

        # ---------- (b) DP over positions with k windows ----------
        INF = 1 << 60
        prev = [0] * (n + 1)              # j = 0
        for j in range(1, k + 1):
            cur = [INF] * (n + 1)
            start = j * x
            for i in range(start, n + 1):
                best = cur[i - 1]
                p = prev[i - x]
                if p < INF:
                    cand = p + cost[i - x]
                    if cand < best:
                        best = cand
                cur[i] = best
            prev = cur
        return prev[n]