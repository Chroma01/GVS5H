import heapq
import random
import sys
from collections import defaultdict
from typing import List


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        # 1. compute cost for each window
        cost = self._compute_costs(nums, x)
        m = len(cost)          # number of possible window starts
        INF = 10**18

        if k == 1:
            return min(cost)

        # ------------------------------------------------------------------
        # 2. DP with a segment tree supporting prefix minimum queries.
        #    dp[t][i] = cost[i] + min_{j <= i-x} dp[t-1][j]
        #    Complexity per DP layer: O(m log m).   Total: O(k * m log m)
        # ------------------------------------------------------------------
        size = 1
        while size < m:
            size <<= 1
        seg = [INF] * (2 * size)

        # bind hot methods locally
        seg_update = self._seg_update
        seg_query  = self._seg_query

        # initialise DP for the first window
        dp_prev = cost[:]                       # t == 1

        for _ in range(2, k + 1):
            # reset segment tree to +inf
            for i in range(2 * size):
                seg[i] = INF

            dp_cur = [INF] * m
            # sweep i from left to right
            for i in range(m):
                prev_start = i - x
                if prev_start >= 0:
                    seg_update(seg, size, prev_start, dp_prev[prev_start])
                    best_prev = seg_query(seg, size, prev_start)
                    if best_prev != INF:
                        dp_cur[i] = best_prev + cost[i]
                # else: impossible, leave INF
            dp_prev = dp_cur

        return min(dp_prev)

    # ------------------------------------------------------------------
    # segment‑tree helpers (operate on the list `seg` passed in)
    # ------------------------------------------------------------------
    @staticmethod
    def _seg_update(seg, size, pos, value):
        i = pos + size
        if value < seg[i]:
            seg[i] = value
            i >>= 1
            while i:
                new_val = seg[i << 1]
                if seg[i << 1 | 1] < new_val:
                    new_val = seg[i << 1 | 1]
                seg[i] = new_val
                i >>= 1

    @staticmethod
    def _seg_query(seg, size, r):
        # minimum over [0 .. r]  (r >= 0)
        INF = 10**18
        res = INF
        i = size          # left pointer (0)
        j = r + size      # right pointer
        while i <= j:
            if i & 1:
                if seg[i] < res:
                    res = seg[i]
                i += 1
            if not (j & 1):
                if seg[j] < res:
                    res = seg[j]
                j -= 1
            i >>= 1
            j >>= 1
        return res

    # ------------------------------------------------------------------
    # Sliding‑window cost using two heaps + lazy deletion + prefix sums
    # ------------------------------------------------------------------
    def _compute_costs(self, nums: List[int], x: int) -> List[int]:
        n = len(nums)
        m = n - x + 1
        if m <= 0:
            return []

        # local aliases for speed
        heappush = heapq.heappush
        heappop  = heapq.heappop
        INF = 10**18

        lo = []          # max‑heap (store negatives)
        hi = []          # min‑heap
        delayed = defaultdict(int)
        sum_lo = 0
        sum_hi = 0

        def prune(heap):
            while heap and delayed[heap[0]] > 0:
                val = heappop(heap)
                cnt = delayed[val] - 1
                if cnt:
                    delayed[val] = cnt
                else:
                    del delayed[val]

        def rebalance():
            nonlocal sum_lo, sum_hi
            # ensure len(lo) == ceil(x/2) and lo holds the smaller half
            if len(lo) > len(hi) + 1:
                val = heappop(lo)
                sum_lo -= val
                heappush(hi, val)
                sum_hi += val
                prune(lo)
            elif len(lo) < len(hi):
                val = heappop(hi)
                sum_hi -= val
                heappush(lo, -val)
                sum_lo += val
                prune(hi)

        # initialise first window
        first = nums[:x]
        for v in first:
            if not lo or v <= -lo[0]:
                heappush(lo, -v)
                sum_lo += v
            else:
                heappush(hi, v)
                sum_hi += v
            rebalance()

        def current_cost():
            m_val = -lo[0]
            # cost = sum |a - median|  =  median*|lo| - sum_lo  +  sum_hi - median*|hi|
            return m_val * len(lo) - sum_lo + sum_hi - m_val * len(hi)

        costs = [current_cost()]

        # slide the window
        for i in range(x, n):
            add_val = nums[i]
            if not lo or add_val <= -lo[0]:
                heappush(lo, -add_val)
                sum_lo += add_val
            else:
                heappush(hi, add_val)
                sum_hi += add_val

            rem_val = nums[i - x]
            if lo and rem_val <= -lo[0]:
                delayed[-rem_val] = delayed.get(-rem_val, 0) + 1
                sum_lo -= rem_val
            else:
                delayed[rem_val] = delayed.get(rem_val, 0) + 1
                sum_hi -= rem_val

            prune(lo)
            prune(hi)
            rebalance()
            prune(lo)
            prune(hi)

            costs.append(current_cost())

        return costs

    # ------------------------------------------------------------------
    # Naive helpers used for self‑testing
    # ------------------------------------------------------------------
    @staticmethod
    def _naive_cost(nums: List[int], x: int) -> List[int]:
        n = len(nums)
        m = n - x + 1
        costs = []
        for i in range(m):
            window = sorted(nums[i:i + x])
            mid = window[x // 2]
            costs.append(sum(abs(v - mid) for v in window))
        return costs

    @staticmethod
    def _naive_min_ops(nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        windows = []
        for i in range(n - x + 1):
            w = nums[i:i + x]
            w_sorted = sorted(w)
            mid = w_sorted[x // 2]
            windows.append(sum(abs(v - mid) for v in w))

        INF = 10**18
        m = len(windows)
        dp_prev = windows[:]          # t == 1
        if k == 1:
            return min(dp_prev)

        for _ in range(2, k + 1):
            dp_cur = [INF] * m
            for i in range(m):
                if i - x >= 0:
                    prev_min = INF
                    limit = i - x + 1
                    for j in range(limit):
                        if dp_prev[j] < prev_min:
                            prev_min = dp_prev[j]
                    if prev_min != INF:
                        dp_cur[i] = prev_min + windows[i]
            dp_prev = dp_cur
        return min(dp_prev)

    # ------------------------------------------------------------------
    # Self‑test / verification harness
    # ------------------------------------------------------------------
    def _self_test(self, trials: int = 200, max_n: int = 30, max_val: int = 20):
        for _ in range(trials):
            n = random.randint(2, max_n)
            x = random.randint(2, n)
            max_k = n // x
            k = random.randint(1, max_k) if max_k > 0 else 1
            nums = [random.randint(-max_val, max_val) for _ in range(n)]

            opt_cost = self._compute_costs(nums, x)
            naive_cost = self._naive_cost(nums, x)
            assert opt_cost == naive_cost, (
                f"Cost mismatch! nums={nums}, x={x}\nopt={opt_cost}\nnaive={naive_cost}"
            )

            fast_ans = self.minOperations(nums, x, k)
            brute_ans = self._naive_min_ops(nums, x, k)
            assert fast_ans == brute_ans, (
                f"DP mismatch! nums={nums}, x={x}, k={k}\n"
                f"fast={fast_ans}, brute={brute_ans}"
            )
        print(f"All {trials} random tests passed.")

    # ------------------------------------------------------------------
    # Large‑scale stress test (runtime check)
    # ------------------------------------------------------------------
    def _stress_test(self, n: int = 100_000, x: int = 500, k: int = 15,
                     max_val: int = 10**6):
        nums = [random.randint(-max_val, max_val) for _ in range(n)]
        ans = self.minOperations(nums, x, k)
        print(f"Stress test n={n}, x={x}, k={k} -> answer={ans}")


if __name__ == "__main__":
    sol = Solution()
    sol._self_test()
    # quick runtime sanity check on maximum input size
    import time
    t0 = time.time()
    sol._stress_test()
    print(f"Stress test runtime: {time.time() - t0:.3f}s")