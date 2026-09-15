from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)

        # Coordinate compression: every window median is one of the original values.
        vals = sorted(set(nums))
        m = len(vals)
        comp = {v: i + 1 for i, v in enumerate(vals)}
        idxs = [comp[v] for v in nums]

        # Fenwick trees:
        # bit_cnt stores frequencies, bit_sum stores sums of original values.
        bit_cnt = [0] * (m + 1)
        bit_sum = [0] * (m + 1)

        def add(idx: int, dc: int, ds: int) -> None:
            while idx <= m:
                bit_cnt[idx] += dc
                bit_sum[idx] += ds
                idx += idx & -idx

        def prefix(idx: int):
            c = 0
            s = 0
            while idx > 0:
                c += bit_cnt[idx]
                s += bit_sum[idx]
                idx -= idx & -idx
            return c, s

        # Highest power of two <= m, for Fenwick kth-order-statistic search.
        top_bit = 1 << (m.bit_length() - 1)

        def kth(target: int) -> int:
            """Return 1-based compressed index of the target-th smallest element."""
            idx = 0
            bit = top_bit
            while bit:
                nxt = idx + bit
                if nxt <= m and bit_cnt[nxt] < target:
                    idx = nxt
                    target -= bit_cnt[nxt]
                bit >>= 1
            return idx + 1

        total = 0
        for i in range(x):
            v = nums[i]
            add(idxs[i], 1, v)
            total += v

        # Lower median rank. For even x, any median between the two middle values
        # has the same absolute-deviation cost.
        target_rank = (x + 1) // 2
        costs = []

        def window_cost() -> int:
            med_idx = kth(target_rank)
            med = vals[med_idx - 1]
            c_le, s_le = prefix(med_idx)

            # Sum of (med - value) for value <= med
            # plus sum of (value - med) for value > med.
            return med * c_le - s_le + (total - s_le) - med * (x - c_le)

        costs.append(window_cost())

        # Slide the window and compute all length-x window costs.
        for i in range(x, n):
            out = nums[i - x]
            add(idxs[i - x], -1, -out)
            total -= out

            inn = nums[i]
            add(idxs[i], 1, inn)
            total += inn

            costs.append(window_cost())

        # DP over prefixes.
        # dp[t][i] = minimum cost to choose t non-overlapping windows
        # inside the first i elements.
        INF = 10 ** 30
        prev = [0] * (n + 1)  # dp for 0 windows

        for t in range(1, k + 1):
            curr = [INF] * (n + 1)

            # At least t*x elements are needed to contain t windows of length x.
            for i in range(t * x, n + 1):
                # Skip current element.
                best = curr[i - 1]

                # Take the window ending at i, starting at i - x.
                cand = prev[i - x] + costs[i - x]
                if cand < best:
                    best = cand

                curr[i] = best

            prev = curr

        return prev[n]