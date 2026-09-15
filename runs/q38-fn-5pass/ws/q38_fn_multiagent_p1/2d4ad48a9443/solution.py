from typing import List
from array import array


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0

        a = nums

        # nxt[i] = first index to the right with a strictly greater value,
        # or n if none exists. Equal values do not create a new prefix maximum.
        nxt = [n] * (n + 1)
        stack = []
        for i in range(n - 1, -1, -1):
            v = a[i]
            while stack and a[stack[-1]] <= v:
                stack.pop()
            if stack:
                nxt[i] = stack[-1]
            stack.append(i)

        # Prefix sums of original elements.
        pref = [0] * (n + 1)
        s = 0
        for i, v in enumerate(a):
            s += v
            pref[i + 1] = s

        # jump[0][i] is the sum of prefix maxima contributed by the record
        # starting at i, from i up to nxt[i] - 1.
        sum0 = [0] * (n + 1)
        for i in range(n):
            sum0[i] = a[i] * (nxt[i] - i)

        # Binary lifting over the next-greater record chain.
        # up[j][i] is the position after 2^j record jumps from i.
        # jump[j][i] is the sum of whole record intervals covered by those jumps.
        LOG = n.bit_length()
        up = [nxt]
        jump = [array('q', sum0)]
        del sum0, stack

        for _ in range(1, LOG):
            pu = up[-1]
            ps = jump[-1]

            cu = [pu[mid] for mid in pu]
            cs = array('q', [ps[i] + ps[mid] for i, mid in enumerate(pu)])

            up.append(cu)
            jump.append(cs)

        # Store levels in descending order for fast queries.
        levels = [(up[j], jump[j]) for j in range(LOG - 1, -1, -1)]
        del up, jump

        def max_sum(l: int, r: int, levels=levels, arr=a) -> int:
            """Sum of running maxima over nums[l..r]."""
            target = r + 1
            cur = l
            res = 0

            for upj, sumj in levels:
                nxt_cur = upj[cur]
                if nxt_cur <= target:
                    res += sumj[cur]
                    cur = nxt_cur

            if cur < target:
                res += arr[cur] * (target - cur)

            return res

        ans = 0
        r = -1
        pref_local = pref
        limit = k
        nonnegative = limit >= 0

        # Two pointers. For fixed l, cost is nondecreasing in r.
        # For fixed r, removing the left endpoint cannot increase cost,
        # so the maximum valid r never decreases as l advances.
        for l in range(n):
            if r < l - 1:
                r = l - 1

            base = pref_local[l]

            while r + 1 < n:
                rr = r + 1

                # A single element always needs 0 increments when k >= 0.
                if rr == l and nonnegative:
                    r = rr
                    continue

                cost = max_sum(l, rr) - pref_local[rr + 1] + base
                if cost <= limit:
                    r = rr
                else:
                    break

            if r >= l:
                ans += r - l + 1

        return ans


def _brute_count(nums, k):
    n = len(nums)
    ans = 0
    for i in range(n):
        mx = nums[i]
        cost = 0
        for j in range(i, n):
            if nums[j] > mx:
                mx = nums[j]
            cost += mx - nums[j]
            if cost <= k:
                ans += 1
            else:
                break
    return ans


def _run_tests():
    sol = Solution()
    failures = []

    cases = [
        ([6, 3, 1, 2, 4, 4], 7, 17),
        ([6, 3, 1, 3, 6], 4, 12),
        ([5], 0, 1),
        ([5], 1, 1),
        ([2, 2, 2], 0, 6),
        ([1, 2, 3, 4], 0, 10),
        ([4, 3, 2, 1], 0, 4),
        ([2, 2, 1], 0, 4),
        ([1, 2, 2, 3], 0, 10),
        ([1, 2, 1, 2], 0, 6),
        ([4, 3, 2, 1], 10**9, 10),
    ]

    for nums, k, expected in cases:
        got = sol.countNonDecreasingSubarrays(nums, k)
        if got != expected:
            failures.append((nums, k, expected, got))

    import random
    random.seed(123456789)

    for _ in range(300):
        n = random.randint(1, 8)
        nums = [random.randint(1, 5) for _ in range(n)]
        k = random.randint(0, 10)
        expected = _brute_count(nums, k)
        got = sol.countNonDecreasingSubarrays(nums, k)
        if got != expected:
            failures.append((nums, k, expected, got))

    if failures:
        print("FAIL")
        for nums, k, expected, got in failures[:10]:
            print(f"nums={nums} k={k} expected={expected} got={got}")
    else:
        print("PASS")


if __name__ == "__main__":
    _run_tests()