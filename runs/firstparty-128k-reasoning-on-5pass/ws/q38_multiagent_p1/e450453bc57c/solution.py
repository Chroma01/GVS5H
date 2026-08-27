from typing import List
import random
from itertools import product, combinations


class Fenwick:
    __slots__ = ("n", "tree", "bitmask")

    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)
        self.bitmask = 1 << (n.bit_length() - 1)

    def add(self, i: int, delta: int) -> None:
        n = self.n
        tree = self.tree
        while i <= n:
            tree[i] += delta
            i += i & -i

    def query(self, i: int) -> int:
        s = 0
        tree = self.tree
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

    def kth(self, k: int) -> int:
        idx = 0
        bitmask = self.bitmask
        tree = self.tree
        n = self.n
        while bitmask:
            nxt = idx + bitmask
            if nxt <= n and tree[nxt] < k:
                idx = nxt
                k -= tree[nxt]
            bitmask >>= 1
        return idx + 1


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)

        vals = sorted(set(nums))
        comp = {v: i + 1 for i, v in enumerate(vals)}
        comp_idx = [comp[v] for v in nums]
        m = len(vals)

        bit_cnt = Fenwick(m)
        bit_sum = Fenwick(m)

        add_cnt = bit_cnt.add
        add_sum = bit_sum.add
        query_cnt = bit_cnt.query
        query_sum = bit_sum.query
        find_kth = bit_cnt.kth

        total_sum = 0
        for i in range(x):
            v = nums[i]
            idx = comp_idx[i]
            add_cnt(idx, 1)
            add_sum(idx, v)
            total_sum += v

        window_count = n - x + 1
        costs = [0] * window_count
        kth_pos = (x + 1) // 2
        last = window_count - 1

        for start in range(window_count):
            med_idx = find_kth(kth_pos)
            med = vals[med_idx - 1]

            cnt_le = query_cnt(med_idx)
            sum_le = query_sum(med_idx)

            costs[start] = total_sum - 2 * sum_le + med * (2 * cnt_le - x)

            if start < last:
                old = nums[start]
                new = nums[start + x]

                if old != new:
                    old_idx = comp_idx[start]
                    new_idx = comp_idx[start + x]

                    add_cnt(old_idx, -1)
                    add_sum(old_idx, -old)
                    total_sum -= old

                    add_cnt(new_idx, 1)
                    add_sum(new_idx, new)
                    total_sum += new

        INF = 10 ** 30
        prev = [0] * (n + 1)
        c = costs

        for j in range(1, k + 1):
            cur = [INF] * (n + 1)
            min_i = j * x

            for i in range(min_i, n + 1):
                idx = i - x
                best = cur[i - 1]

                pv = prev[idx]
                if pv < INF:
                    cand = pv + c[idx]
                    if cand < best:
                        best = cand

                cur[i] = best

            prev = cur

        return prev[n]


def _has_k_equal_windows(arr: List[int], x: int, k: int) -> bool:
    n = len(arr)
    dp = [0] * (n + 1)
    for i in range(x, n + 1):
        dp[i] = dp[i - 1]
        first = arr[i - x]
        ok = True
        for j in range(i - x + 1, i):
            if arr[j] != first:
                ok = False
                break
        if ok:
            cand = dp[i - x] + 1
            if cand > dp[i]:
                dp[i] = cand
    return dp[n] >= k


def brute_force_selection(nums: List[int], x: int, k: int) -> int:
    n = len(nums)
    INF = 10 ** 30
    candidates = sorted(set(nums))
    wcost = [0] * (n - x + 1)

    for s in range(n - x + 1):
        best = INF
        for t in candidates:
            c = 0
            for p in range(s, s + x):
                c += abs(nums[p] - t)
            if c < best:
                best = c
        wcost[s] = best

    best = INF
    for starts in combinations(range(n - x + 1), k):
        ok = True
        for i in range(k - 1):
            if starts[i] + x > starts[i + 1]:
                ok = False
                break
        if not ok:
            continue

        total = 0
        for s in starts:
            total += wcost[s]
            if total >= best:
                break
        if total < best:
            best = total

    return best


def brute_force_full(nums: List[int], x: int, k: int) -> int:
    n = len(nums)
    lo = min(nums)
    hi = max(nums)

    if (hi - lo + 1) ** n > 20000:
        return brute_force_selection(nums, x, k)

    best = sum(abs(v - lo) for v in nums)

    for arr in product(range(lo, hi + 1), repeat=n):
        cost = 0
        for i in range(n):
            cost += abs(arr[i] - nums[i])
            if cost >= best:
                break
        if cost >= best:
            continue

        if _has_k_equal_windows(arr, x, k):
            best = cost

    return best


def run_tests() -> None:
    sol = Solution()

    assert sol.minOperations([5, -2, 1, 3, 7, 3, 6, 4, -1], 3, 2) == 8
    assert sol.minOperations([9, -2, -2, -2, 1, 5], 2, 2) == 3

    assert sol.minOperations([1, 2], 2, 1) == 1
    assert sol.minOperations([1, 2, 3, 4, 5], 5, 1) == 6
    assert sol.minOperations([-5, -1, -3], 3, 1) == 4
    assert sol.minOperations([0, 1000000, -1000000], 3, 1) == 2000000
    assert sol.minOperations([0, 10, 0, 10], 2, 2) == 20
    assert sol.minOperations([1, 1, 2, 2], 2, 2) == 0
    assert sol.minOperations([1, 2, 1, 2], 2, 2) == 2
    assert sol.minOperations([-2, -2, -1, -1], 2, 2) == 0
    assert sol.minOperations([-2, -1, -2, -1], 2, 2) == 2
    assert sol.minOperations([1, 2, 3], 2, 1) == 1
    assert sol.minOperations([1, 100, 1], 3, 1) == 99
    assert sol.minOperations([100, 0, 0, 100, 0], 2, 2) == 100
    assert sol.minOperations([0, 1] * 15, 2, 15) == 15

    large = [0] * 100000
    assert sol.minOperations(large, 100000, 1) == 0
    assert sol.minOperations(large, 50000, 2) == 0

    rng = random.Random(12345)

    for _ in range(80):
        n = rng.randint(2, 6)
        x = rng.randint(2, n)
        max_k = n // x
        k = rng.randint(1, max_k)
        nums = [rng.randint(-2, 2) for _ in range(n)]
        expected = brute_force_full(nums, x, k)
        got = sol.minOperations(nums, x, k)
        if expected != got:
            raise AssertionError(
                f"full brute mismatch: nums={nums}, x={x}, k={k}, "
                f"expected={expected}, got={got}"
            )

    for _ in range(200):
        n = rng.randint(2, 12)
        x = rng.randint(2, n)
        max_k = n // x
        k = rng.randint(1, min(15, max_k))
        if rng.random() < 0.5:
            nums = [rng.randint(-3, 3) for _ in range(n)]
        else:
            nums = [rng.randint(-10**6, 10**6) for _ in range(n)]
        expected = brute_force_selection(nums, x, k)
        got = sol.minOperations(nums, x, k)
        if expected != got:
            raise AssertionError(
                f"selection brute mismatch: nums={nums}, x={x}, k={k}, "
                f"expected={expected}, got={got}"
            )

    print("All tests passed.")


if __name__ == "__main__":
    run_tests()