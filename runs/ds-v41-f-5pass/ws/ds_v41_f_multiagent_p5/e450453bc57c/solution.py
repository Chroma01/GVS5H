from typing import List
import time
import random
import tracemalloc


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)

        # Coordinate compression
        vals = sorted(set(nums))
        U = len(vals)
        rank = {v: i + 1 for i, v in enumerate(vals)}

        bit_cnt = [0] * (U + 1)
        bit_sum = [0] * (U + 1)

        # Initialize first window [0, x) -- Fenwick ops inlined for speed
        total = 0
        for i in range(x):
            v = nums[i]
            total += v
            j = rank[v]
            while j <= U:
                bit_cnt[j] += 1
                bit_sum[j] += v
                j += j & -j

        w = n - x + 1
        cost = [0] * w
        med_pos = (x + 1) // 2          # 1-indexed lower median
        top = 1 << (U.bit_length() - 1)

        for i in range(w):
            if i:
                # slide: remove nums[i-1], add nums[i+x-1]
                ov = nums[i - 1]
                total -= ov
                j = rank[ov]
                while j <= U:
                    bit_cnt[j] -= 1
                    bit_sum[j] -= ov
                    j += j & -j

                nv = nums[i + x - 1]
                total += nv
                j = rank[nv]
                while j <= U:
                    bit_cnt[j] += 1
                    bit_sum[j] += nv
                    j += j & -j

            # k-th order statistic (med_pos) via Fenwick binary lifting
            idx = 0
            step = top
            order = med_pos
            while step:
                nxt = idx + step
                if nxt <= U and bit_cnt[nxt] < order:
                    idx = nxt
                    order -= bit_cnt[nxt]
                step >>= 1
            m = vals[idx]        # median value
            rm = idx + 1         # its 1-indexed compressed rank (= rank[m])

            cnt_le = 0
            j = rm
            while j > 0:
                cnt_le += bit_cnt[j]
                j -= j & -j
            sum_le = 0
            j = rm
            while j > 0:
                sum_le += bit_sum[j]
                j -= j & -j

            cost[i] = total - 2 * sum_le + 2 * m * cnt_le - m * x

        # DP over exactly k non-overlapping windows
        INF = 10 ** 30
        dp = cost                      # t = 1
        for _ in range(2, k + 1):
            pref_min = [0] * w
            mn = INF
            for i in range(w):
                di = dp[i]
                if di < mn:
                    mn = di
                pref_min[i] = mn
            ndp = [INF] * w
            for i in range(x, w):
                ndp[i] = cost[i] + pref_min[i - x]
            dp = ndp

        return min(dp)


# ------------------------------------------------------------------
# Verification / benchmarking harness
# ------------------------------------------------------------------

INF_SENTINEL = 10 ** 30


def make_array(n: int, mode: str, seed: int = 12345):
    rnd = random.Random(seed)
    if mode == "distinct":
        a = [-1000000 + i * 20 for i in range(n)]   # n distinct values in [-1e6, 1e6]
        rnd.shuffle(a)
        return a
    if mode == "random":
        return [rnd.randint(-1000000, 1000000) for _ in range(n)]
    if mode == "equal":
        return [12345] * n
    raise ValueError(mode)


def main():
    sol = Solution()

    # --- correctness sanity on the two provided examples ---
    assert sol.minOperations([5, -2, 1, 3, 7, 3, 6, 4, -1], 3, 2) == 8
    assert sol.minOperations([9, -2, -2, -2, 1, 5], 2, 2) == 3
    print("Example checks: PASS")

    n = 100000
    scenarios = [
        ("distinct x=2    k=15", 2, 15, "distinct"),
        ("distinct x=500  k=15", 500, 15, "distinct"),
        ("distinct x=5000 k=15", 5000, 15, "distinct"),
        ("distinct x=6666 k=15", 6666, 15, "distinct"),
        ("random   x=1000 k=15", 1000, 15, "random"),
        ("equal    x=1000 k=15", 1000, 15, "equal"),
    ]
    overall = True
    print("=== Performance at n=100000 ===")
    for desc, x, k, mode in scenarios:
        nums = make_array(n, mode)
        kk = k if k * x <= n else n // x
        t0 = time.perf_counter()
        ans = sol.minOperations(nums, x, kk)
        t1 = time.perf_counter()
        dt = t1 - t0
        ok = 0 <= ans < INF_SENTINEL
        overall &= ok
        print(f"{desc}: ans={ans} time={dt:.3f}s {'PASS' if ok else 'FAIL'}")

    print("=== Memory (distinct x=2 k=15) ===")
    nums = make_array(n, "distinct")
    tracemalloc.start()
    sol.minOperations(nums, 2, 15)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"peak traced memory: {peak / 1e6:.1f} MB")

    print("=== INF handling ===")
    rnd = random.Random(2024)
    fails = 0
    cnt = 0
    for _ in range(2000):
        nn = rnd.randint(2, 80)
        xx = rnd.randint(2, nn)
        maxk = nn // xx
        if maxk < 1:
            continue
        kk = rnd.randint(1, maxk)
        arr = [rnd.randint(-30, 30) for _ in range(nn)]
        ans = sol.minOperations(arr, xx, kk)
        cnt += 1
        if not (0 <= ans < INF_SENTINEL):
            fails += 1
    print(f"random feasible small grids ({cnt} cases): {'PASS' if fails == 0 else 'FAIL'} ({fails} fails)")
    overall &= fails == 0

    # tight packing: n == k*x exactly (max stress on DP feasibility)
    for x, k in [(6666, 15), (9999, 10), (50000, 2), (2, 15)]:
        nn = x * k
        arr = make_array(nn, "distinct")
        ans = sol.minOperations(arr, x, k)
        ok = 0 <= ans < INF_SENTINEL
        overall &= ok
        print(f"tight packing n={nn} x={x} k={k}: ans={ans} {'PASS' if ok else 'FAIL'}")

    print("=== OVERALL:", "PASS" if overall else "FAIL", "===")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())