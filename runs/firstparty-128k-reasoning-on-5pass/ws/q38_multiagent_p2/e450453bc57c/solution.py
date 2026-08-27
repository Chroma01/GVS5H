from typing import List
import heapq
import random


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        m = n - x + 1

        low = []      # max-heap: (-value, index)
        high = []     # min-heap: (value, index)

        in_low = bytearray(n)
        removed = bytearray(n)

        low_sum = 0
        total_sum = 0
        size_low = 0
        size_high = 0

        heappush = heapq.heappush
        heappop = heapq.heappop

        def clean_low():
            while low and removed[low[0][1]]:
                heappop(low)

        def clean_high():
            while high and removed[high[0][1]]:
                heappop(high)

        def rebalance():
            nonlocal size_low, size_high, low_sum

            if size_low < size_high:
                clean_high()
                val, idx = heappop(high)
                size_high -= 1

                heappush(low, (-val, idx))
                in_low[idx] = 1
                size_low += 1
                low_sum += val

            elif size_low > size_high + 1:
                clean_low()
                negval, idx = heappop(low)
                val = -negval
                size_low -= 1
                low_sum -= val

                heappush(high, (val, idx))
                in_low[idx] = 0
                size_high += 1

        def add(idx):
            nonlocal total_sum, size_low, size_high, low_sum

            val = nums[idx]
            total_sum += val

            if size_low == 0:
                heappush(low, (-val, idx))
                in_low[idx] = 1
                low_sum += val
                size_low += 1
            else:
                clean_low()
                if val <= -low[0][0]:
                    heappush(low, (-val, idx))
                    in_low[idx] = 1
                    low_sum += val
                    size_low += 1
                else:
                    heappush(high, (val, idx))
                    in_low[idx] = 0
                    size_high += 1

            rebalance()

        def remove(idx):
            nonlocal total_sum, size_low, size_high, low_sum

            val = nums[idx]
            total_sum -= val

            if in_low[idx]:
                size_low -= 1
                low_sum -= val
            else:
                size_high -= 1

            removed[idx] = 1
            rebalance()

        def window_cost():
            clean_low()
            med = -low[0][0]
            return (
                med * size_low
                - low_sum
                + (total_sum - low_sum)
                - med * size_high
            )

        costs = [0] * m

        for i in range(x):
            add(i)
        costs[0] = window_cost()

        for start in range(1, m):
            add(start + x - 1)
            remove(start - 1)
            costs[start] = window_cost()

        sentinel = 10 ** 30
        prev = [0] * (n + 1)

        for chosen in range(1, k + 1):
            cur = [sentinel] * (n + 1)
            start_i = chosen * x

            p = prev
            c = cur
            cst = costs
            xx = x

            for i in range(start_i, n + 1):
                best = c[i - 1]
                s = i - xx
                candidate = p[s] + cst[s]
                if candidate < best:
                    best = candidate
                c[i] = best

            prev = cur

        return prev[n]


def brute_force(nums: List[int], x: int, k: int) -> int:
    n = len(nums)
    m = n - x + 1
    costs = []

    for s in range(m):
        window = nums[s:s + x]
        med = sorted(window)[(x - 1) // 2]
        costs.append(sum(abs(v - med) for v in window))

    INF = 10 ** 30
    best = INF

    def dfs(min_start: int, chosen: int, total: int) -> None:
        nonlocal best
        if total >= best:
            return
        if chosen == k:
            best = total
            return

        remaining = k - chosen
        max_start = n - remaining * x
        stop = min(m, max_start + 1)

        for s in range(min_start, stop):
            dfs(s + x, chosen + 1, total + costs[s])

    dfs(0, 0, 0)
    return best


def run_validation() -> None:
    sol = Solution()
    failures = []

    def check(name, nums, x, k, expected=None):
        try:
            got = sol.minOperations(nums, x, k)
        except Exception as exc:
            failures.append(f"{name}: exception {exc!r}")
            return

        if expected is None:
            expected = brute_force(nums, x, k)

        if got != expected:
            failures.append(
                f"{name}: nums={nums} x={x} k={k} expected={expected} got={got}"
            )

    check("example1", [5, -2, 1, 3, 7, 3, 6, 4, -1], 3, 2, 8)
    check("example2", [9, -2, -2, -2, 1, 5], 2, 2, 3)

    check("x_equals_n", [1, 2, 3], 3, 1, 2)
    check("x_equals_n_negative", [-5, -1, -3], 3, 1, 4)
    check("x_equals_n_even", [1, 100, 2, 3], 4, 1, 100)
    check("adjacent_windows", [0, 10, 0, 10], 2, 2, 20)
    check("all_equal", [7, 7, 7, 7], 2, 2, 0)
    check("k_one", [1, 100, 2], 3, 1, 99)
    check("negative_adjacent", [-1, 10, -1, 10], 2, 2, 22)
    check("large_values", [10 ** 6, -10 ** 6, 0], 3, 1, 2000000)
    check("max_k_adjacent", [0] * 30, 2, 15, 0)
    check("max_k_nonzero", list(range(30)), 2, 15, 15)

    random.seed(123456)
    for t in range(5000):
        n = random.randint(2, 8)
        x = random.randint(2, n)
        max_k = n // x
        k = random.randint(1, max_k)
        nums = [random.randint(-5, 5) for _ in range(n)]
        check(f"random_small_{t}", nums, x, k)

    random.seed(654321)
    for t in range(2000):
        n = random.randint(2, 12)
        x = random.randint(2, n)
        max_k = n // x
        k = random.randint(1, max_k)
        nums = [random.randint(-10, 10) for _ in range(n)]
        check(f"random_medium_{t}", nums, x, k)

    if failures:
        print("FAIL")
        for item in failures[:10]:
            print(item)
    else:
        print("PASS")


if __name__ == "__main__":
    run_validation()