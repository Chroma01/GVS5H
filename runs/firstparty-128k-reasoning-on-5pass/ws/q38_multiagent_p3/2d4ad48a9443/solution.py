import random
from typing import List
from array import array


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0
        if n == 1:
            return 1 if k >= 0 else 0

        n1 = n + 1

        # ng[i] = nearest next index j > i with nums[j] > nums[i], or n.
        ng = [n] * n1
        stack = []
        for i in range(n - 1, -1, -1):
            vi = nums[i]
            while stack and nums[stack[-1]] <= vi:
                stack.pop()
            if stack:
                ng[i] = stack[-1]
            stack.append(i)
        del stack

        # Base binary-lifting table and prefix sums.
        up0 = array('i', ng)
        pref = [0] * n1
        c0 = array('q', [0]) * n1
        running = 0
        for i, x in enumerate(nums):
            running += x
            pref[i + 1] = running
            c0[i] = x * (ng[i] - i)
        del ng

        LOG = n1.bit_length()
        up = [up0]
        contrib = [c0]

        # Build binary lifting tables.
        for _ in range(1, LOG):
            prev_u = up[-1]
            prev_c = contrib[-1]
            curr_u = array('i', [n]) * n1
            curr_c = array('q', [0]) * n1
            for i, mid in enumerate(prev_u):
                curr_u[i] = prev_u[mid]
                curr_c[i] = prev_c[i] + prev_c[mid]
            up.append(curr_u)
            contrib.append(curr_c)

        rev_tables = tuple((up[t], contrib[t]) for t in range(LOG - 1, -1, -1))
        del up, contrib

        def too_expensive(l, r, rev_tables=rev_tables, pref=pref, nums=nums, k=k):
            if l == r:
                return 0 > k

            r1 = r + 1
            limit = k + (pref[r1] - pref[l])
            pos = l
            total = 0

            for up_t, contrib_t in rev_tables:
                nxt = up_t[pos]
                if nxt <= r1:
                    total += contrib_t[pos]
                    if total > limit:
                        return True
                    pos = nxt
                    if pos >= r1:
                        break

            if pos < r1:
                total += nums[pos] * (r1 - pos)

            return total > limit

        ans = 0
        left = 0
        for right in range(n):
            while left <= right and too_expensive(left, right):
                left += 1
            ans += right - left + 1

        return ans


def brute_force(nums: List[int], k: int) -> int:
    n = len(nums)
    ans = 0
    for l in range(n):
        mx = -10**30
        cost = 0
        for r in range(l, n):
            v = nums[r]
            if v > mx:
                mx = v
            cost += mx - v
            if cost <= k:
                ans += 1
    return ans


def run_tests() -> None:
    sol = Solution()
    failures = []
    passed = 0

    def check(name, nums, k, expected=None, verbose=True):
        nonlocal passed
        got = sol.countNonDecreasingSubarrays(nums, k)
        want = brute_force(nums, k)
        ok = (got == want)
        if expected is not None:
            ok = ok and (got == expected)
        if ok:
            passed += 1
            if verbose:
                print(f"PASS {name}: got={got}")
        else:
            msg = f"FAIL {name}: nums={nums}, k={k}, got={got}, brute={want}"
            if expected is not None:
                msg += f", expected={expected}"
            print(msg)
            failures.append(msg)

    def summary(name, start_passed, start_failures):
        total = (passed - start_passed) + (len(failures) - start_failures)
        if len(failures) == start_failures:
            print(f"PASS {name}: {passed - start_passed}/{total}")
        else:
            print(f"FAIL {name}: {passed - start_passed}/{total}")

    check("example1", [6, 3, 1, 2, 4, 4], 7, 17)
    check("example2", [6, 3, 1, 3, 6], 4, 12)
    summary("examples", 0, 0)

    start_passed = passed
    start_failures = len(failures)
    check("n0", [], 0, 0)
    check("n1_k0", [5], 0, 1)
    check("n1_k1", [5], 1, 1)
    check("all_equal_k0", [7, 7, 7, 7, 7], 0, 15)
    check("all_equal_k1", [7, 7, 7, 7, 7], 1, 15)
    check("strictly_increasing_k0", [1, 2, 3, 4, 5], 0, 15)
    check("strictly_decreasing_k0", [5, 4, 3, 2, 1], 0, 5)
    check("strictly_decreasing_k1", [5, 4, 3, 2, 1], 1, 9)
    check("k_larger_than_all_costs", [3, 1, 2, 1], 100, 10)
    check("k0_mixed", [2, 2, 1, 2], 0, 6)
    check("k1_mixed", [2, 2, 1, 2], 1, 10)
    summary("edge_cases", start_passed, start_failures)

    rng = random.Random(12345)

    start_passed = passed
    start_failures = len(failures)
    for i in range(2000):
        n = rng.randint(1, 8)
        nums = [rng.randint(1, 10) for _ in range(n)]
        k = rng.randint(0, 20)
        check(f"random_small_{i}", nums, k, verbose=False)
    summary("random_small", start_passed, start_failures)

    start_passed = passed
    start_failures = len(failures)
    for i in range(200):
        n = rng.randint(9, 20)
        nums = [rng.randint(1, 100) for _ in range(n)]
        k = rng.randint(0, 500)
        check(f"random_medium_{i}", nums, k, verbose=False)
    summary("random_medium", start_passed, start_failures)

    start_passed = passed
    start_failures = len(failures)
    for i in range(500):
        n = rng.randint(1, 10)
        nums = [rng.randint(1, 10) for _ in range(n)]
        check(f"random_k0_{i}", nums, 0, verbose=False)
    summary("random_k0", start_passed, start_failures)

    start_passed = passed
    start_failures = len(failures)
    for i in range(200):
        n = rng.randint(1, 10)
        nums = [rng.randint(1, 100) for _ in range(n)]
        check(f"random_large_k_{i}", nums, 10**9, verbose=False)
    summary("random_large_k", start_passed, start_failures)

    if failures:
        print(f"OVERALL FAIL: {len(failures)} failing case(s)")
        for msg in failures:
            print(msg)
    else:
        print(f"OVERALL PASS: {passed} tests passed, 0 failing cases")


if __name__ == "__main__":
    run_tests()