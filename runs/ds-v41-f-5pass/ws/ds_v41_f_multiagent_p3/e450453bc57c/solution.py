from typing import List


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)

        # --- coordinate compression ---
        vals = sorted(set(nums))
        comp = {v: i + 1 for i, v in enumerate(vals)}
        m = len(vals)
        cv = [comp[v] for v in nums]

        # two Fenwick trees over compressed values: counts and sums
        cnt = [0] * (m + 1)
        sm = [0] * (m + 1)
        LOG = 1 << (m.bit_length())

        num_windows = n - x + 1
        cost = [0] * num_windows
        total = 0
        target = (x + 1) // 2  # rank of the lower median

        for i in range(n):
            v = nums[i]
            j = cv[i]
            while j <= m:
                cnt[j] += 1
                sm[j] += v
                j += j & (-j)
            total += v

            if i >= x:
                w = nums[i - x]
                j = cv[i - x]
                while j <= m:
                    cnt[j] -= 1
                    sm[j] -= w
                    j += j & (-j)
                total -= w

            if i >= x - 1:
                # kth-smallest via Fenwick binary lifting, accumulating
                # count and sum of elements strictly below the median
                idx = 0
                t = target
                cl = 0
                sl = 0
                bm = LOG
                while bm:
                    nxt = idx + bm
                    if nxt <= m:
                        c = cnt[nxt]
                        if c < t:
                            idx = nxt
                            t -= c
                            cl += c
                            sl += sm[nxt]
                    bm >>= 1
                median = vals[idx]
                # cost = sum |a-median| = 2*(median*cl - sl) + total - median*x
                cost[i - x + 1] = 2 * (median * cl - sl) + total - median * x

        # --- DP: exactly k non-overlapping windows ---
        INF = float('inf')
        prev = [0] * (n + 1)  # j = 0
        for _ in range(k):
            cur = [INF] * (n + 1)
            for i in range(x, n + 1):
                best = cur[i - 1]
                p = prev[i - x]
                if p != INF:
                    cand = p + cost[i - x]
                    if cand < best:
                        best = cand
                cur[i] = best
            prev = cur

        return prev[n]