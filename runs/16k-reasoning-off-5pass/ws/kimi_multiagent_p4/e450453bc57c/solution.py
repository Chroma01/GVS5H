from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)

        # Coordinate compression
        coords = sorted(set(nums))
        comp = {v: i + 1 for i, v in enumerate(coords)}  # 1-indexed
        m = len(coords)

        # Fenwick trees for count and sum
        bit_count = [0] * (m + 1)
        bit_sum = [0] * (m + 1)

        def update(bit, idx, delta):
            while idx <= m:
                bit[idx] += delta
                idx += idx & -idx

        def query(bit, idx):
            s = 0
            while idx > 0:
                s += bit[idx]
                idx -= idx & -idx
            return s

        def kth_element(kth):
            # smallest idx such that prefix count >= kth (1-indexed kth)
            idx = 0
            bitmask = 1 << (m.bit_length())
            while bitmask:
                nxt = idx + bitmask
                if nxt <= m and bit_count[nxt] < kth:
                    kth -= bit_count[nxt]
                    idx = nxt
                bitmask >>= 1
            return idx + 1

        # Initialize first window [0, x)
        for i in range(x):
            c = comp[nums[i]]
            update(bit_count, c, 1)
            update(bit_sum, c, nums[i])

        # cost[i] = min operations to make window nums[i..i+x-1] all equal
        cost = [0] * (n - x + 1)

        def window_cost():
            # median: element of rank (x+1)//2 (1-indexed)
            rank = (x + 1) // 2
            midx = kth_element(rank)
            median = coords[midx - 1]
            left_count = query(bit_count, midx - 1)
            left_sum = query(bit_sum, midx - 1)
            right_count = query(bit_count, m) - query(bit_count, midx)
            right_sum = query(bit_sum, m) - query(bit_sum, midx)
            # elements equal to median need 0 ops
            return median * left_count - left_sum + right_sum - median * right_count

        cost[0] = window_cost()
        for i in range(1, n - x + 1):
            # remove nums[i-1], add nums[i+x-1]
            out_v = nums[i - 1]
            in_v = nums[i + x - 1]
            update(bit_count, comp[out_v], -1)
            update(bit_sum, comp[out_v], -out_v)
            update(bit_count, comp[in_v], 1)
            update(bit_sum, comp[in_v], in_v)
            cost[i] = window_cost()

        # DP: f[i][j] = min cost using first i elements (nums[0..i-1]) with j subarrays
        # f[i][j] = min(f[i-1][j], f[i-x][j-1] + cost[i-x])
        INF = float('inf')
        f = [[INF] * (k + 1) for _ in range(n + 1)]
        f[0][0] = 0
        for i in range(1, n + 1):
            f[i][0] = 0
            for j in range(1, k + 1):
                f[i][j] = f[i - 1][j]
                if i - x >= 0 and f[i - x][j - 1] != INF:
                    cand = f[i - x][j - 1] + cost[i - x]
                    if cand < f[i][j]:
                        f[i][j] = cand
        return f[n][k]