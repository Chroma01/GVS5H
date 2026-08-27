from typing import List
import sys
import time
import math
import random

try:
    import resource
except ImportError:
    resource = None

try:
    import tracemalloc
except ImportError:
    tracemalloc = None


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)

        pref = [0] * (n + 1)
        for i, x in enumerate(nums):
            pref[i + 1] = pref[i] + x

        # ng[i] = first index to the right with strictly greater value, or n.
        ng = [n] * (n + 1)
        stack = []
        for i in range(n - 1, -1, -1):
            xi = nums[i]
            while stack and nums[stack[-1]] <= xi:
                stack.pop()
            if stack:
                ng[i] = stack[-1]
            stack.append(i)
        ng[n] = n
        del stack

        # root_cost[i] = minimal cost to make nums[i..n-1] non-decreasing
        # using running maxima starting at i.
        root_cost = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            j = ng[i]
            root_cost[i] = nums[i] * (j - i) - (pref[j] - pref[i]) + root_cost[j]

        # Binary lifting over the next-greater chain.
        LOG = (n + 1).bit_length()
        up = [ng]
        for _ in range(1, LOG):
            prev = up[-1]
            up.append([prev[prev[i]] for i in range(n + 1)])

        levels = tuple(range(LOG - 1, -1, -1))

        def cost(l: int, r: int,
                 up=up, root_cost=root_cost, nums=nums, pref=pref,
                 levels=levels) -> int:
            R = r + 1
            p = l

            # Farthest next-greater ancestor still inside [l, r].
            for j in levels:
                q = up[j][p]
                if q <= R:
                    p = q

            # Complete segments before p.
            res = root_cost[l] - root_cost[p]

            # Partial segment from p to r, if any.
            if p <= r:
                res += nums[p] * (R - p) - (pref[R] - pref[p])

            return res

        ans = 0
        left = 0
        for r in range(n):
            while left <= r and cost(left, r) > k:
                left += 1
            ans += r - left + 1
        return ans


def total_subarrays(n: int) -> int:
    return n * (n + 1) // 2


def expected_strictly_decreasing(n: int, k: int) -> int:
    # For consecutive strictly decreasing values, length L costs L*(L-1)//2.
    m = (1 + math.isqrt(1 + 8 * k)) // 2
    while m * (m - 1) // 2 > k:
        m -= 1
    while (m + 1) * m // 2 <= k:
        m += 1
    if m > n:
        m = n
    return m * (n + 1) - m * (m + 1) // 2


def peak_rss_mib() -> float:
    if resource is None:
        return float("nan")
    ru = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return ru / (1024.0 * 1024.0)
    return ru / 1024.0


def brute_count(nums: List[int], k: int) -> int:
    n = len(nums)
    ans = 0
    for l in range(n):
        mx = nums[l]
        c = 0
        for r in range(l, n):
            if nums[r] > mx:
                mx = nums[r]
            c += mx - nums[r]
            if c <= k:
                ans += 1
            else:
                break
    return ans


def run_case(name: str, nums: List[int], k: int, expected, sol: Solution) -> bool:
    n = len(nums)
    total = total_subarrays(n)

    use_tm = resource is None and tracemalloc is not None
    if use_tm:
        tracemalloc.start()

    start = time.perf_counter()
    ans = sol.countNonDecreasingSubarrays(nums, k)
    elapsed = time.perf_counter() - start

    if use_tm:
        peak, _ = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        rss = peak / (1024.0 * 1024.0)
    else:
        rss = peak_rss_mib()

    ok = True
    if expected is not None and ans != expected:
        ok = False
    if not (n <= ans <= total):
        ok = False

    exp_text = "bounds" if expected is None else str(expected)
    print(
        f"{name}: n={n} k={k} ans={ans} expected={exp_text} "
        f"time={elapsed:.3f}s peak_rss={rss:.1f}MiB "
        f"{'OK' if ok else 'FAIL'}"
    )
    return ok


def run_small_checks(sol: Solution) -> bool:
    cases = [
        ([6, 3, 1, 2, 4, 4], 7, 17),
        ([6, 3, 1, 3, 6], 4, 12),
        ([1], 1, 1),
        ([2, 1], 0, 2),
        ([2, 1], 1, 3),
        ([3, 2, 1], 0, 3),
        ([3, 2, 1], 1, 5),
        ([3, 2, 1], 3, 6),
        ([5, 5, 5], 0, 6),
        ([1, 3, 2], 0, 4),
        ([1, 3, 2], 1, 6),
        ([10**9, 1, 10**9], 0, 4),
        ([10**9, 1, 10**9], 999999999, 6),
    ]

    ok = True
    for nums, k, exp in cases:
        got = sol.countNonDecreasingSubarrays(nums, k)
        if got != exp:
            ok = False
            print(f"small fixed FAIL nums={nums} k={k} expected={exp} actual={got}")

    random.seed(987654321)
    for _ in range(200):
        n = random.randint(1, 9)
        nums = [random.randint(1, 12) for _ in range(n)]
        k = random.randint(0, 30)
        exp = brute_count(nums, k)
        got = sol.countNonDecreasingSubarrays(nums, k)
        if got != exp:
            ok = False
            print(f"small random FAIL nums={nums} k={k} expected={exp} actual={got}")

    print(f"small checks: {'OK' if ok else 'FAIL'}")
    return ok


def main() -> None:
    sol = Solution()
    small_ok = run_small_checks(sol)

    n = 100000
    total = total_subarrays(n)
    large_ok = True
    large_start = time.perf_counter()

    random.seed(123456789)
    random_large = [random.randint(1, 10**9) for _ in range(n)]
    large_ok &= run_case("random_large_k1e9", random_large, 10**9, None, sol)
    large_ok &= run_case("random_large_khuge", random_large, 10**18, total, sol)
    del random_large

    inc = list(range(10**9 - n + 1, 10**9 + 1))
    large_ok &= run_case("strictly_increasing_large", inc, 10**9, total, sol)
    del inc

    dec = list(range(10**9, 10**9 - n, -1))
    dec_k = 10**9
    large_ok &= run_case(
        "strictly_decreasing_large",
        dec,
        dec_k,
        expected_strictly_decreasing(n, dec_k),
        sol,
    )
    del dec

    eq = [10**9] * n
    large_ok &= run_case("all_equal_large", eq, 10**9, total, sol)
    del eq

    print(f"total large time={time.perf_counter() - large_start:.3f}s")
    print(f"LARGE SANITY: {'PASS' if small_ok and large_ok else 'FAIL'}")


if __name__ == "__main__":
    main()