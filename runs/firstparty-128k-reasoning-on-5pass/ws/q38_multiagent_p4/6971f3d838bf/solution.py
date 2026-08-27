from typing import List
from collections import defaultdict, Counter
import random


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        NEG = -10**18

        # Power-of-two iterative segment tree.
        size = 1
        while size < n:
            size <<= 1
        m = size << 1

        # For each node, store the non-empty max-subarray summary of active leaves:
        # total sum, best prefix, best suffix, best subarray.
        # best == NEG means the segment has no active element.
        total = [0] * m
        pref = [NEG] * m
        suff = [NEG] * m
        best = [NEG] * m

        base = size
        for i, v in enumerate(nums):
            p = base + i
            total[p] = v
            pref[p] = v
            suff[p] = v
            best[p] = v

        # Build initial tree with all elements active.
        for p in range(base - 1, 0, -1):
            l = p << 1
            r = l + 1
            bl = best[l]
            br = best[r]

            if bl == NEG:
                total[p] = total[r]
                pref[p] = pref[r]
                suff[p] = suff[r]
                best[p] = br
            elif br == NEG:
                total[p] = total[l]
                pref[p] = pref[l]
                suff[p] = suff[l]
                best[p] = bl
            else:
                tl = total[l]
                tr = total[r]
                total[p] = tl + tr

                a = pref[l]
                b = tl + pref[r]
                pref[p] = a if a >= b else b

                a = suff[r]
                b = tr + suff[l]
                suff[p] = a if a >= b else b

                b = bl
                if br > b:
                    b = br
                c = suff[l] + pref[r]
                if c > b:
                    b = c
                best[p] = b

        ans = best[1]

        # Only negative values can improve the answer.
        neg_indices = defaultdict(list)
        for i, v in enumerate(nums):
            if v < 0:
                neg_indices[v].append(i)

        if not neg_indices:
            return ans

        def set_active(i, active,
                       total=total, pref=pref, suff=suff, best=best,
                       nums=nums, base=base, NEG=NEG):
            p = base + i
            if active:
                v = nums[i]
                total[p] = v
                pref[p] = v
                suff[p] = v
                best[p] = v
            else:
                total[p] = 0
                pref[p] = NEG
                suff[p] = NEG
                best[p] = NEG

            p >>= 1
            while p:
                l = p << 1
                r = l + 1
                bl = best[l]
                br = best[r]

                if bl == NEG:
                    total[p] = total[r]
                    pref[p] = pref[r]
                    suff[p] = suff[r]
                    best[p] = br
                elif br == NEG:
                    total[p] = total[l]
                    pref[p] = pref[l]
                    suff[p] = suff[l]
                    best[p] = bl
                else:
                    tl = total[l]
                    tr = total[r]
                    total[p] = tl + tr

                    a = pref[l]
                    b = tl + pref[r]
                    pref[p] = a if a >= b else b

                    a = suff[r]
                    b = tr + suff[l]
                    suff[p] = a if a >= b else b

                    b = bl
                    if br > b:
                        b = br
                    c = suff[l] + pref[r]
                    if c > b:
                        b = c
                    best[p] = b

                p >>= 1

        for v, indices in neg_indices.items():
            # Cannot delete the only value in the array.
            if len(indices) < n:
                for i in indices:
                    set_active(i, False)

                cur = best[1]
                if cur > ans:
                    ans = cur

                for i in indices:
                    set_active(i, True)

        return ans


def _max_subarray(arr: List[int]) -> int:
    if not arr:
        return 0
    best = cur = arr[0]
    for x in arr[1:]:
        cur = max(x, cur + x)
        if cur > best:
            best = cur
    return best


def _brute_force(nums: List[int]) -> int:
    n = len(nums)
    ans = _max_subarray(nums)

    for x, cnt in Counter(nums).items():
        if cnt < n:
            filtered = [a for a in nums if a != x]
            ans = max(ans, _max_subarray(filtered))

    return ans


def _run_tests() -> None:
    sol = Solution()

    tests = [
        ([-3, 2, -2, -1, 3, -2, 3], 7),
        ([1, 2, 3, 4], 10),
        ([5], 5),
        ([-5], -5),
        ([0], 0),
        ([2, 2, 2], 6),
        ([-2, -2, -2], -2),
        ([0, 0, 0], 0),
        ([-5, -1, -3], -1),
        ([1, 2, 3], 6),
        ([0, -1, 0], 0),
        ([-1, 0, -2], 0),
        ([5, -2, 0, 5], 10),
        ([-1, 2, -3, 2, -1], 4),
        ([-1, -2, -3], -1),
        ([-1, 100, -1, 100, -1], 200),
        ([0, 1, 0, 2], 3),
        ([2, -1, 2], 4),
        ([1, -2, 1, -2, 1], 3),
        ([-5, -1, -5], -1),
        ([-1, 5, -1, 5, -1], 10),
        ([-1000000, 1000000, -1000000, 1000000], 2000000),
    ]

    failures = []

    for nums, expected in tests:
        got = sol.maxSubarraySum(nums)
        if got != expected:
            failures.append((nums, expected, got))

    rng = random.Random(20240525)

    def check(nums: List[int]) -> None:
        got = sol.maxSubarraySum(nums)
        expected = _brute_force(nums)
        if got != expected:
            failures.append((nums, expected, got))

    # Small arrays with a small alphabet to force repeated values.
    for _ in range(3000):
        n = rng.randint(1, 9)
        check([rng.randint(-4, 4) for _ in range(n)])
        if len(failures) >= 5:
            break

    # Medium arrays with a slightly larger alphabet.
    for _ in range(200):
        n = rng.randint(1, 20)
        check([rng.randint(-6, 6) for _ in range(n)])
        if len(failures) >= 5:
            break

    # Small arrays with large values to check sum bounds.
    for _ in range(200):
        n = rng.randint(1, 12)
        check([rng.randint(-10**6, 10**6) for _ in range(n)])
        if len(failures) >= 5:
            break

    if failures:
        print("FAILURES:")
        for nums, expected, got in failures[:5]:
            print(f"nums={nums} expected={expected} got={got}")
        raise SystemExit(1)

    print("All tests passed: examples, edge cases, and 3400 random brute-force checks.")


if __name__ == "__main__":
    _run_tests()