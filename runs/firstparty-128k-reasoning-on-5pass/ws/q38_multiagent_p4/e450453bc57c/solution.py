from typing import List


class Fenwick:
    __slots__ = ("n", "tree")

    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, i: int, delta: int) -> None:
        n = self.n
        tree = self.tree
        while i <= n:
            tree[i] += delta
            i += i & -i

    def sum(self, i: int) -> int:
        s = 0
        tree = self.tree
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

    def kth(self, k: int) -> int:
        idx = 0
        bit = 1 << (self.n.bit_length() - 1)
        tree = self.tree
        n = self.n
        while bit:
            nxt = idx + bit
            if nxt <= n and tree[nxt] < k:
                idx = nxt
                k -= tree[nxt]
            bit >>= 1
        return idx + 1


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        if k == 0:
            return 0
        if x <= 0 or x > n or k * x > n:
            return 0

        vals = sorted(set(nums))
        comp = {v: i + 1 for i, v in enumerate(vals)}
        idxs = [comp[v] for v in nums]
        m = len(vals)

        bit_count = Fenwick(m)
        bit_sum = Fenwick(m)

        bc_add = bit_count.add
        bs_add = bit_sum.add
        bc_sum = bit_count.sum
        bs_sum = bit_sum.sum
        bc_kth = bit_count.kth

        costs = [0] * (n - x + 1)
        half = (x + 1) // 2
        total_sum = 0

        for i, v in enumerate(nums):
            idx = idxs[i]
            bc_add(idx, 1)
            bs_add(idx, v)
            total_sum += v

            if i >= x:
                old = nums[i - x]
                old_idx = idxs[i - x]
                bc_add(old_idx, -1)
                bs_add(old_idx, -old)
                total_sum -= old

            if i >= x - 1:
                med_idx = bc_kth(half)
                med = vals[med_idx - 1]
                left_count = bc_sum(med_idx)
                left_sum = bs_sum(med_idx)
                right_count = x - left_count
                right_sum = total_sum - left_sum
                costs[i - x + 1] = (
                    med * left_count - left_sum
                    + right_sum - med * right_count
                )

        INF = 10 ** 30
        prev = [0] * (n + 1)
        n_plus_1 = n + 1

        for t in range(1, k + 1):
            cur = [INF] * n_plus_1
            start = t * x
            for i in range(start, n_plus_1):
                best = cur[i - 1]
                cand = prev[i - x] + costs[i - x]
                if cand < best:
                    best = cand
                cur[i] = best
            prev = cur

        return prev[n]