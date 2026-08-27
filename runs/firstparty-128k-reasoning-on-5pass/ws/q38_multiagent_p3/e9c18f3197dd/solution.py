from typing import List
from math import gcd
import random
import time


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1
        size = 1 << m

        # lcm[mask] = lcm of the targets whose bits are set in mask
        lcm = [1] * size
        for mask in range(1, size):
            bit = mask & -mask
            i = bit.bit_length() - 1
            prev = mask ^ bit
            a = lcm[prev]
            b = target[i]
            lcm[mask] = a // gcd(a, b) * b

        # Precompute all transitions: from a covered mask, choose a nonempty
        # submask of still-uncovered targets to cover with the current element.
        trans = [[] for _ in range(size)]
        for mask in range(size):
            rem = full ^ mask
            sub = rem
            while sub:
                trans[mask].append((sub, mask | sub))
                sub = (sub - 1) & rem

        # Since target.length <= nums.length, we can always assign distinct
        # nums elements to target indices. Each such increment costs at most
        # target[i] - 1, so the optimum is strictly below this cap.
        INF = sum(target) - m + 1

        dp = [INF] * size
        dp[0] = 0

        for x in nums:
            # cost[sub] = minimum increments to make x a multiple of lcm[sub]
            cost = [INF] * size
            for sub in range(1, size):
                L = lcm[sub]
                c = (L - x % L) % L
                if c < INF:
                    cost[sub] = c

            # Option 1: leave this nums element unused.
            ndp = dp[:]

            # Option 2: use this nums element to cover one nonempty subset
            # of currently uncovered targets.
            for mask, base in enumerate(dp):
                if base >= INF:
                    continue
                for sub, new_mask in trans[mask]:
                    c = cost[sub]
                    if c >= INF:
                        continue
                    val = base + c
                    if val < ndp[new_mask]:
                        ndp[new_mask] = val

            dp = ndp

            if dp[full] == 0:
                return 0

        return dp[full]


def brute_force(nums: List[int], target: List[int]) -> int:
    """
    Independent oracle for small cases.

    Under the constraints, a feasible solution exists by assigning distinct
    nums elements to target entries, with total cost at most
    sum(target) - len(target). Therefore every element in some optimal
    solution is incremented by at most C = sum(target) - len(target).

    For each original value x, enumerate x and all multiples of target values
    in [x, x + C]. Any optimal final value either is x or is a multiple of at
    least one target, so this enumeration is complete. Then combine exact
    coverage masks with a separate DP.
    """
    m = len(target)
    size = 1 << m
    full = size - 1
    INF = 10**18

    if len(target) <= len(nums):
        C = sum(target) - len(target)
    else:
        # Fallback for invalid small tests; not used under the constraints.
        C = sum(target) * 2 + max(nums) if nums else 0

    dp = [INF] * size
    dp[0] = 0

    for x in nums:
        best = [INF] * size
        candidates = {x}
        limit = x + C

        for t in target:
            start = ((x + t - 1) // t) * t
            if start <= limit:
                candidates.update(range(start, limit + 1, t))

        for y in candidates:
            mask = 0
            for i, t in enumerate(target):
                if y % t == 0:
                    mask |= 1 << i
            c = y - x
            if c < best[mask]:
                best[mask] = c

        ndp = [INF] * size
        for m0, base in enumerate(dp):
            if base >= INF:
                continue
            for m1, c in enumerate(best):
                if c >= INF:
                    continue
                nm = m0 | m1
                val = base + c
                if val < ndp[nm]:
                    ndp[nm] = val
        dp = ndp

    return dp[full]


def main() -> int:
    sol = Solution()
    failures = []

    def check(name: str, nums: List[int], target: List[int], expected: int | None = None) -> None:
        actual = sol.minimumIncrements(nums, target)
        ok = True
        detail = f"actual={actual}"

        bf = None
        if len(nums) <= 10 and sum(target) <= 50000:
            bf = brute_force(nums, target)

        if expected is not None and actual != expected:
            ok = False
            detail += f" expected={expected}"

        if bf is not None and actual != bf:
            ok = False
            detail += f" brute={bf}"

        if ok:
            print(f"PASS {name}: {detail}")
        else:
            print(f"FAIL {name}: {detail}")
            failures.append(f"{name}: {detail}")

    # Provided examples.
    check("example1", [1, 2, 3], [4], 1)
    check("example2", [8, 4], [10, 5], 2)
    check("example3", [7, 9, 10], [7], 0)

    # Edge cases.
    check("already_satisfied", [6, 1], [2, 3], 0)
    check("one_covers_all", [12, 1], [3, 4, 6], 0)
    check("target_one", [101, 1], [1, 100], 99)
    check("duplicate_targets_zero", [5, 1], [5, 5], 0)
    check("duplicate_targets_one", [4, 6], [5, 5], 1)
    check("duplicate_targets_three", [4, 100, 100], [5, 5, 5], 1)
    check("all_ones", [1, 2, 3], [1, 1, 1], 0)
    check("nums_larger", [10000], [9999], 9998)
    check("target_larger", [1], [10000], 9999)
    check("one_element_covers_two", [8, 101], [5, 10], 2)
    check("mixed_redundant", [11, 100], [6, 7], 5)
    check("large_lcm_small_nums", [1, 1, 1, 1], [9999, 10000, 9998, 9997], 39990)
    check("large_lcm_large_nums", [10000, 10000, 10000, 10000], [9999, 10000, 9998, 9997], None)
    check("many_unused", [1, 2, 3, 4, 5, 6], [6], 0)
    check("need_increment", [1, 2, 3], [5], 2)

    # Randomized brute-force checks.
    random.seed(12345)
    random_cases = 1000
    random_failures = 0

    for i in range(random_cases):
        n = random.randint(1, 6)
        t = random.randint(1, min(4, n))
        nums = [random.randint(1, 8) for _ in range(n)]
        target = [random.randint(1, 8) for _ in range(t)]

        actual = sol.minimumIncrements(nums, target)
        expected = brute_force(nums, target)

        if actual != expected:
            random_failures += 1
            if len(failures) < 10:
                failures.append(
                    f"random case {i}: nums={nums} target={target} "
                    f"actual={actual} brute={expected}"
                )

    print(f"randomized: {random_cases - random_failures}/{random_cases} passed")
    if random_failures:
        failures.append(f"randomized failures: {random_failures}")

    # Maximum-size performance test.
    n = 50000
    nums = [1] * n
    target = [9999, 10000, 9998, 9997]

    start = time.perf_counter()
    perf_ans = sol.minimumIncrements(nums, target)
    elapsed = time.perf_counter() - start

    print(f"performance: n={n} t={len(target)} answer={perf_ans} elapsed={elapsed:.3f}s")
    if elapsed > 10.0:
        failures.append(f"performance too slow: {elapsed:.3f}s")

    print()
    if failures:
        print(f"FAILURES: {len(failures)}")
        for f in failures[:20]:
            print(f"  {f}")
        return 1

    print("ALL TESTS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())