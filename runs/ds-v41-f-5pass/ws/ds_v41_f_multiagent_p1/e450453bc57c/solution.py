from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        vals = sorted(set(nums))
        comp = {v: i + 1 for i, v in enumerate(vals)}
        size = len(vals)

        # Fenwick trees over compressed ranks: one for counts, one for value sums
        bit_c = [0] * (size + 1)
        bit_s = [0] * (size + 1)

        def add(i, dc, ds):
            while i <= size:
                bit_c[i] += dc
                bit_s[i] += ds
                i += i & (-i)

        def pref(i):
            c = 0
            s = 0
            while i > 0:
                c += bit_c[i]
                s += bit_s[i]
                i -= i & (-i)
            return c, s

        # highest power of two <= size
        top = 1
        while top * 2 <= size:
            top <<= 1

        def kth(kk):
            # smallest rank whose prefix count >= kk
            idx = 0
            b = top
            while b:
                nxt = idx + b
                if nxt <= size and bit_c[nxt] < kk:
                    idx = nxt
                    kk -= bit_c[nxt]
                b >>= 1
            return idx + 1

        mrank = (x + 1) // 2  # lower median position (1-indexed)

        # initialize window nums[0:x]
        for i in range(x):
            v = nums[i]
            add(comp[v], 1, v)
        total = sum(nums[:x])

        costs = [0] * (n - x + 1)

        for s in range(n - x + 1):
            r = kth(mrank)
            c_le, s_le = pref(r)
            m = vals[r - 1]
            costs[s] = (m * c_le - s_le) + ((total - s_le) - m * (x - c_le))
            if s < n - x:
                old = nums[s]
                add(comp[old], -1, -old)
                total -= old
                new = nums[s + x]
                add(comp[new], 1, new)
                total += new

        INF = 10 ** 30
        prev = [0] * (n + 1)  # t = 0: zero cost using any prefix
        for _ in range(k):
            cur = [INF] * (n + 1)
            for i in range(x, n + 1):
                best = cur[i - 1]
                cand = prev[i - x] + costs[i - x]
                if cand < best:
                    best = cand
                cur[i] = best
            prev = cur
        return prev[n]