import heapq
import random
import sys
import time
from collections import defaultdict
from typing import List


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        m = n - x + 1  # number of possible window starts

        # ---------- Step 1: cost[s] = min ops to make nums[s:s+x] constant ----------
        # For a fixed window the optimal target is a median, cost = sum |a - median|.
        # Maintain a sliding median with two heaps + lazy deletion, tracking sums.
        lo = []  # max-heap (store negated values), holds the smaller half
        hi = []  # min-heap, holds the larger half
        delayed = defaultdict(int)
        lo_size = hi_size = 0
        sum_lo = sum_hi = 0

        def prune(heap, is_lo):
            while heap:
                val = -heap[0] if is_lo else heap[0]
                if delayed[val] > 0:
                    delayed[val] -= 1
                    heapq.heappop(heap)
                else:
                    break

        def rebalance():
            nonlocal lo_size, hi_size, sum_lo, sum_hi
            if lo_size > hi_size + 1:
                v = -heapq.heappop(lo)
                sum_lo -= v
                heapq.heappush(hi, v)
                sum_hi += v
                lo_size -= 1
                hi_size += 1
            elif lo_size < hi_size:
                v = heapq.heappop(hi)
                sum_hi -= v
                heapq.heappush(lo, -v)
                sum_lo += v
                hi_size -= 1
                lo_size += 1

        def add(num):
            nonlocal lo_size, hi_size, sum_lo, sum_hi
            if lo and num <= -lo[0]:
                heapq.heappush(lo, -num)
                sum_lo += num
                lo_size += 1
            else:
                heapq.heappush(hi, num)
                sum_hi += num
                hi_size += 1
            rebalance()
            prune(lo, True)
            prune(hi, False)

        def remove(num):
            nonlocal lo_size, hi_size, sum_lo, sum_hi
            delayed[num] += 1
            if lo and num <= -lo[0]:
                lo_size -= 1
                sum_lo -= num
            else:
                hi_size -= 1
                sum_hi -= num
            # clean tops before rebalancing so rebalance pops valid elements
            prune(lo, True)
            prune(hi, False)
            rebalance()
            prune(lo, True)
            prune(hi, False)

        def window_cost():
            med = -lo[0]
            return med * lo_size - sum_lo + sum_hi - med * hi_size

        cost = [0] * m
        for i in range(x):
            add(nums[i])
        cost[0] = window_cost()
        for s in range(1, m):
            remove(nums[s - 1])
            add(nums[s + x - 1])
            cost[s] = window_cost()

        # ---------- Step 2: pick k non-overlapping windows with min total cost ----------
        # prev[s] = min cost to choose t-1 windows with all starts <= s (prefix min).
        # cur[s]  = min(cur[s-1], prev[s-x] + cost[s])  (previous start <= s-x).
        INF = 10**30
        prev = [0] * m  # t = 0: zero windows cost 0 everywhere
        for t in range(1, k + 1):
            cur = [INF] * m
            for s in range(m):
                best = cur[s - 1] if s > 0 else INF
                if s >= x:
                    base = prev[s - x]
                else:
                    base = 0 if t == 1 else INF
                cand = base + cost[s]
                if cand < best:
                    best = cand
                cur[s] = best
            prev = cur

        return prev[m - 1]


# ============ Independent reference implementations ============

def ref_window_costs(nums, x):
    """Sort-based per-window costs; fully independent of the two-heap structure."""
    n = len(nums)
    out = []
    for s in range(n - x + 1):
        w = sorted(nums[s:s + x])
        med = w[x // 2]  # any median is optimal (upper median for even x)
        out.append(sum(abs(v - med) for v in w))
    return out


def reference_min_ops(nums, x, k):
    """Min total cost over ALL non-overlapping subsets of size >= k.

    Exact-t DP: dp[s] = min cost choosing exactly t windows with the t-th
    window starting exactly at s. Computes EVERY feasible t (1..n//x) and
    takes the min over t >= k, so it does NOT assume 'at least k == exactly k'.
    """
    n = len(nums)
    m = n - x + 1
    costs = ref_window_costs(nums, x)
    INF = float('inf')
    max_t = n // x
    ans = INF
    dp = costs[:]  # t = 1
    for t in range(1, max_t + 1):
        if t > 1:
            pref = [INF] * m
            run = INF
            for s in range(m):
                if dp[s] < run:
                    run = dp[s]
                pref[s] = run
            new = [INF] * m
            for s in range(x, m):
                if pref[s - x] < INF:
                    new[s] = pref[s - x] + costs[s]
            dp = new
        if t >= k:
            cur = min(dp)
            if cur < ans:
                ans = cur
    return ans


def exhaustive_min_ops(nums, x, k):
    """Exponential enumeration of every non-overlapping subset (tiny inputs)."""
    n = len(nums)
    m = n - x + 1
    costs = ref_window_costs(nums, x)
    best = [None]

    def rec(s, chosen, total):
        if chosen >= k:
            if best[0] is None or total < best[0]:
                best[0] = total
        if s >= m:
            return
        if best[0] is not None and total >= best[0]:
            return  # costs are nonnegative: cannot improve
        rec(s + 1, chosen, total)
        rec(s + x, chosen + 1, total + costs[s])

    rec(0, 0, 0)
    return best[0]


# ============ Test drivers ============

def run_boundary_tests(sol):
    """Directed edge/boundary cases, incl. k=15 and tight k*x == n packings."""
    directed = [
        # (nums, x, k, expected or None -> use reference)
        ([5, -2, 1, 3, 7, 3, 6, 4, -1], 3, 2, 8),        # example 1
        ([9, -2, -2, -2, 1, 5], 2, 2, 3),                # example 2
        (list(range(30)), 2, 15, 15),                    # k=15, tight k*x==n
        ([(i % 3) - 1 for i in range(45)], 3, 15, None), # k=15 tight, duplicates
        ([(i * 7) % 11 - 5 for i in range(300)], 20, 15, None),  # k=15 tight, big x
        ([7] * 30, 2, 15, 0),                            # all equal, tight -> 0
        ([1, -1] * 15, 2, 15, 30),                       # alternating, tight
        ([0] * 60, 4, 15, 0),                            # zeros, even x, tight
        ([3, 1, 4, 1, 5, 9, 2, 6], 8, 1, None),          # x == n, k == 1
        ([3, 1, 4, 1, 5, 9, 2, 6], 7, 1, None),          # x == n-1
        ([(i % 5) - 2 for i in range(200)], 5, 15, None),# k=15, loose packing
        ([2, 2, 1, 1, 2, 2, 1, 1], 4, 2, None),          # duplicates, even x
        ([-5, -5, -5, -5, -5, -5], 3, 2, 0),             # all-equal negatives
        ([10, -10, 10, -10], 2, 2, 40),                  # large swings, tight
    ]
    trials = 0
    for nums, x, k, expected in directed:
        if expected is None:
            expected = reference_min_ops(nums, x, k)
        got = sol.minOperations(nums, x, k)
        trials += 1
        if got != expected:
            print(f"MISMATCH (boundary): nums={nums[:20]}... x={x} k={k} "
                  f"expected={expected} got={got}")
            return False, trials
        # triple-check tiny cases with exhaustive enumeration
        m = len(nums) - x + 1
        if m <= 18 and k <= 4:
            ex = exhaustive_min_ops(nums, x, k)
            if got != ex:
                print(f"MISMATCH (boundary vs exhaustive): nums={nums} x={x} "
                      f"k={k} exhaustive={ex} got={got}")
                return False, trials
    print(f"boundary tests: {trials} passed")
    return True, trials


def run_random_medium_tests(sol, count=300):
    """Random medium inputs (n up to ~300, k up to 15) vs independent reference."""
    rng = random.Random(31337)
    value_ranges = [(-2, 2), (-5, 5), (0, 3), (-9, -1), (-1, 1),
                    (0, 0), (-100, 100), (-10**6, 10**6)]
    trials = 0
    for _ in range(count):
        x = rng.randint(2, 12)                       # even and odd x
        k = rng.randint(1, 15)                       # full k range
        lo_n = k * x
        n = rng.randint(lo_n, min(lo_n + 25, 300))   # includes tight k*x == n
        lo_v, hi_v = rng.choice(value_ranges)
        nums = [rng.randint(lo_v, hi_v) for _ in range(n)]
        expected = reference_min_ops(nums, x, k)
        got = sol.minOperations(nums, x, k)
        trials += 1
        if got != expected:
            print(f"MISMATCH (medium): nums={nums} x={x} k={k} "
                  f"expected={expected} got={got}")
            return False, trials
    print(f"random medium tests (k up to 15): {trials} passed")
    return True, trials


def run_small_exhaustive_tests(sol, count=250):
    """Tiny random inputs vs fully exhaustive subset enumeration."""
    rng = random.Random(777)
    value_ranges = [(-2, 2), (0, 0), (-1, 1), (-9, -1), (-3, 6)]
    trials = 0
    for _ in range(count):
        x = rng.randint(2, 6)
        k = rng.randint(1, 3)
        n = rng.randint(k * x, k * x + 5)            # m <= 18 keeps it feasible
        lo_v, hi_v = rng.choice(value_ranges)
        nums = [rng.randint(lo_v, hi_v) for _ in range(n)]
        expected = exhaustive_min_ops(nums, x, k)
        got = sol.minOperations(nums, x, k)
        trials += 1
        if got != expected:
            print(f"MISMATCH (exhaustive): nums={nums} x={x} k={k} "
                  f"expected={expected} got={got}")
            return False, trials
    print(f"small exhaustive tests: {trials} passed")
    return True, trials


def run_perf_tests():
    """Max-size (n=1e5, k=15) performance + deterministic sanity checks."""
    n = 100_000
    k = 15
    x_big = n // k                                   # 6666; k*x = 99990 <= n
    rng = random.Random(987654321)
    PERF_LIMIT = 10.0  # generous ceiling; expected ~0.3-1.0s per case

    cases = [
        ("strictly increasing, x=n/k",
         [i * 10 - 500000 for i in range(n)], x_big, k, None),
        ("strictly decreasing, x=n/k",
         [500000 - i * 10 for i in range(n)], x_big, k, None),
        ("random uniform [-1e6,1e6], x=n/k",
         [rng.randint(-10**6, 10**6) for _ in range(n)], x_big, k, None),
        ("all equal, x=n/k",
         [42] * n, x_big, k, 0),
        ("alternating +-1e6, x=n/k",
         [(-10**6) if i % 2 == 0 else 10**6 for i in range(n)], x_big, k, None),
        ("few distinct {-1,0,1} (lazy-deletion stress)",
         [rng.choice((-1, 0, 1)) for _ in range(n)], x_big, k, None),
        ("tight packing k*x == n exactly (n=99990)",
         [rng.randint(-10**6, 10**6) for _ in range(k * x_big)], x_big, k, None),
        ("max DP load: x=2, m=99999, random",
         [rng.randint(-10**6, 10**6) for _ in range(n)], 2, k, None),
        ("increasing step 10, x=2 (closed-form check)",
         [i * 10 - 500000 for i in range(n)], 2, k, 150),
        ("alternating +-1e6, x=2 (closed-form check)",
         [(-10**6) if i % 2 == 0 else 10**6 for i in range(n)], 2, k, 30_000_000),
    ]

    sol = Solution()
    total = 0.0
    for name, nums, x, kk, expected in cases:
        t0 = time.perf_counter()
        res = sol.minOperations(nums, x, kk)
        dt = time.perf_counter() - t0
        total += dt
        ok = isinstance(res, int) and res >= 0 and dt < PERF_LIMIT
        if expected is not None and res != expected:
            ok = False
        print(f"  [{'OK' if ok else 'FAIL'}] {name}: n={len(nums)} x={x} "
              f"k={kk} -> {res} in {dt:.3f}s")
        if not ok:
            print(f"PERF/SANITY FAILURE: {name} (res={res}, expected={expected}, "
                  f"dt={dt:.3f}s)")
            return False
    print(f"perf tests: all {len(cases)} max-size cases passed, "
          f"total {total:.3f}s (limit {PERF_LIMIT}s per case)")
    return True


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    solution = Solution()

    ok, _ = run_boundary_tests(solution)
    if not ok:
        sys.exit(1)
    ok, _ = run_random_medium_tests(solution)
    if not ok:
        sys.exit(1)
    ok, _ = run_small_exhaustive_tests(solution)
    if not ok:
        sys.exit(1)
    if not run_perf_tests():
        sys.exit(1)

    # final sanity on the provided examples
    assert solution.minOperations([5, -2, 1, 3, 7, 3, 6, 4, -1], 3, 2) == 8
    assert solution.minOperations([9, -2, -2, -2, 1, 5], 2, 2) == 3

    print("ALL EDGE/BOUNDARY/PERFORMANCE TESTS PASSED")
    sys.exit(0)