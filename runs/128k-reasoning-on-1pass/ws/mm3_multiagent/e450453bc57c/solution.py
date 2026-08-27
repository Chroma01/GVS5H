from typing import List

class BIT:
    """
    Fenwick Tree (Binary Indexed Tree) that supports:
    - add(idx, delta): point update
    - prefix_sum(idx): sum of first idx elements (1‑based)
    - find_kth(k): order‑statistics (smallest idx such that prefix_sum(idx) >= k)
    All indices are 1‑based.
    """
    def __init__(self, size: int):
        self.n = size
        self.bit = [0] * (self.n + 1)

    def add(self, idx: int, delta):
        """Add delta to position idx (1‑based)."""
        while idx <= self.n:
            self.bit[idx] += delta
            idx += idx & -idx

    def prefix_sum(self, idx: int):
        """Return sum of elements in [1, idx] (1‑based)."""
        res = 0
        while idx:
            res += self.bit[idx]
            idx -= idx & -idx
        return res

    def find_kth(self, k: int):
        """
        Return the smallest index i such that prefix_sum(i) >= k.
        Assumes 1 <= k <= total sum.
        """
        idx = 0
        # largest power of two <= n
        bit_mask = 1 << (self.n.bit_length() - 1)
        while bit_mask:
            nxt = idx + bit_mask
            if nxt <= self.n and self.bit[nxt] < k:
                idx = nxt
                k -= self.bit[nxt]
            bit_mask >>= 1
        return idx + 1


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        """
        Returns the minimum number of +/-1 operations needed to obtain at least k
        non‑overlapping subarrays of length x where all elements inside each subarray
        are equal.
        """
        n = len(nums)
        # ---------- 1. compute cost for every window of length x ----------
        # coordinate compression of values appearing in nums
        sorted_vals = sorted(set(nums))
        val_to_idx = {v: i + 1 for i, v in enumerate(sorted_vals)}  # 1‑based indices
        m = len(sorted_vals)

        freq_bit = BIT(m)          # stores counts of each value
        sum_bit = BIT(m)           # stores the sum of actual values

        # initialise first window
        window_sum = 0
        for i in range(x):
            v = nums[i]
            idx = val_to_idx[v]
            freq_bit.add(idx, 1)
            sum_bit.add(idx, v)
            window_sum += v

        # helper to compute cost for the current window
        def window_cost() -> int:
            rank = (x + 1) // 2                 # lower median
            median_idx = freq_bit.find_kth(rank)   # 1‑based index in compressed space
            median_val = sorted_vals[median_idx - 1]

            # number and sum of elements <= median
            cnt_left = freq_bit.prefix_sum(median_idx)
            sum_left = sum_bit.prefix_sum(median_idx)

            # cost = sum_{i} |a_i - median|
            left_part = median_val * cnt_left - sum_left
            right_part = (window_sum - sum_left) - median_val * (x - cnt_left)
            return left_part + right_part

        costs = []
        # compute cost for the first window
        costs.append(window_cost())

        # slide the window
        for start in range(1, n - x + 1):
            # element leaving the window
            out_val = nums[start - 1]
            out_idx = val_to_idx[out_val]
            freq_bit.add(out_idx, -1)
            sum_bit.add(out_idx, -out_val)
            window_sum -= out_val

            # element entering the window
            in_val = nums[start + x - 1]
            in_idx = val_to_idx[in_val]
            freq_bit.add(in_idx, 1)
            sum_bit.add(in_idx, in_val)
            window_sum += in_val

            costs.append(window_cost())

        # ---------- 2. DP for selecting k non‑overlapping windows ----------
        m = n - x + 1          # number of possible start positions
        INF = 10**18

        # dp_prev[i] = min cost to place t windows using first i elements
        dp_prev = [INF] * (n + 1)
        dp_prev[0] = 0

        for t in range(1, k + 1):
            dp_cur = [INF] * (n + 1)
            # we cannot place a window ending before we have enough elements
            for i in range(1, n + 1):
                if i < x:
                    # not enough elements to form a window of size x
                    dp_cur[i] = INF
                else:
                    # option 1: skip element i-1
                    opt1 = dp_cur[i - 1]
                    # option 2: place a window that ends at i-1
                    # its start is i - x, cost index is (i - x)
                    opt2 = costs[i - x] + dp_prev[i - x]
                    dp_cur[i] = opt1 if opt1 < opt2 else opt2
            dp_prev = dp_cur

        return dp_prev[n]


# ----------------------------------------------------------------------
# Optional simple test harness (not required for the solution itself)
if __name__ == "__main__":
    sol = Solution()

    # Example 1
    nums1 = [5, -2, 1, 3, 7, 3, 6, 4, -1]
    print(sol.minOperations(nums1, 3, 2))   # expected 8

    # Example 2
    nums2 = [9, -2, -2, -2, 1, 5]
    print(sol.minOperations(nums2, 2, 2))   # expected 3