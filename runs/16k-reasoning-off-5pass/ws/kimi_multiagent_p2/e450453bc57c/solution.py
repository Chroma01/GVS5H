from typing import List


class Fenwick:
    __slots__ = ("n", "tree")

    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, i: int, delta) -> None:
        i += 1
        n = self.n
        tree = self.tree
        while i <= n:
            tree[i] += delta
            i += i & (-i)

    def sum(self, i: int):
        # prefix sum over [0, i]
        i += 1
        s = 0
        tree = self.tree
        while i > 0:
            s += tree[i]
            i -= i & (-i)
        return s

    def kth(self, k: int) -> int:
        # smallest index i such that prefix count >= k (1 <= k <= total)
        idx = 0
        bitmask = 1 << (self.n.bit_length() - 1)
        tree = self.tree
        while bitmask:
            nxt = idx + bitmask
            if nxt <= self.n and tree[nxt] < k:
                idx = nxt
                k -= tree[nxt]
            bitmask >>= 1
        return idx  # 0-indexed position in compressed array


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        m = n - x + 1  # number of windows

        # Coordinate compression
        vals = sorted(set(nums))
        comp = {v: i for i, v in enumerate(vals)}
        size = len(vals)
        a = [comp[v] for v in nums]

        cnt = Fenwick(size)
        sm = Fenwick(size)

        # Initialize first window
        for i in range(x):
            cnt.add(a[i], 1)
            sm.add(a[i], nums[i])

        half = (x + 1) // 2  # lower median rank

        def window_cost() -> int:
            med_idx = cnt.kth(half)
            med = vals[med_idx]
            left_cnt = cnt.sum(med_idx)
            left_sum = sm.sum(med_idx)
            total_sum = sm.sum(size - 1)
            right_cnt = x - left_cnt
            right_sum = total_sum - left_sum
            return med * left_cnt - left_sum + right_sum - med * right_cnt

        cost = [0] * m
        cost[0] = window_cost()
        for i in range(1, m):
            out_idx = a[i - 1]
            in_idx = a[i + x - 1]
            cnt.add(out_idx, -1)
            sm.add(out_idx, -nums[i - 1])
            cnt.add(in_idx, 1)
            sm.add(in_idx, nums[i + x - 1])
            cost[i] = window_cost()

        # DP: dp[j][i] = min cost to get j non-overlapping windows using starts <= i
        INF = float("inf")
        prev = [0] * m  # dp[0][i] = 0
        for j in range(1, k + 1):
            cur = [INF] * m
            # earliest start for the j-th window is (j-1)*x
            start = (j - 1) * x
            if start >= m:
                break
            if j == 1:
                cur[start] = cost[start]
            else:
                cur[start] = prev[start - x] + cost[start]
            for i in range(start + 1, m):
                take = prev[i - x] + cost[i] if i - x >= 0 else INF
                skip = cur[i - 1]
                cur[i] = skip if skip < take else take
            prev = cur

        return prev[m - 1]